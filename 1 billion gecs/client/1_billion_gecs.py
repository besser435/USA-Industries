import obg_options
import time
import pydirectinput
import mouse
import keyboard
import pytesseract
import tempfile
import getpass
import requests
import traceback
import urllib.request
import os 
import re
import json
from colorama import init
init()
from colorama import Fore
init(autoreset=True)
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter
from time import sleep
from datetime import datetime
# https://learncodebygaming.com/blog/pyautogui-not-working-use-directinput

# Options in obg_options.py
refill_delay = obg_options.refill_delay
update_on_close = obg_options.update_on_close
username = obg_options.username
app_server_ip = obg_options.app_server_ip
abort_if_in_chat = obg_options.abort_if_in_chat
start_delay = obg_options.start_delay
override_abort = False
#tesseract_path = obg_options.tesseract_path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


version = "v1.4.4"

def refill_picks():
    # move to the dohickey
    pydirectinput.keyDown("s")
    sleep(2)
    pydirectinput.keyUp("s")
    pydirectinput.keyDown("d")
    sleep(5)
    pydirectinput.keyUp("d")

    # discard hotbar items
    for i in range(0, 9):
        pydirectinput.keyDown("ctrl")
        pydirectinput.press("q")    # assumes q is your drop items key
        pydirectinput.keyUp("ctrl")
        mouse.wheel(-1) # cycle hotbar slots. 
        # Would have liked to use a for loop and just hit the slot key (1-9) with the loop index rather than using the scrollwheel,
        # but it skipped slots for some reason. This is the next best thing.

    sleep(0.5)

    # dispense 9 new picks and equip them in the hotbar slot
    for i in range(0, 9):
        pydirectinput.click(button="right") # signals the machine to drop a pick
        mouse.wheel(-1) 
        sleep(0.5)

    sleep(0.5)

    # move to the money machine
    pydirectinput.keyDown("a")
    sleep(1)
    pydirectinput.keyUp("a")

    pydirectinput.keyDown("w")
    sleep(1.5)
    pydirectinput.keyUp("w")

    sleep(0.5)

    print("Refilled picks")


def abort():
    pydirectinput.mouseUp()
    pydirectinput.keyUp("tab")

    pydirectinput.keyDown("alt")
    pydirectinput.press("f4")       
    pydirectinput.keyUp("alt")

    # Update the kill flag on the USA server
    try:
        data = {"kill_flag": True}
        response = requests.post(app_server_ip + "/killflag", json=data)
        if response.status_code == 200:
            print("Kill flag updated successfully.")
        else:
            print(Fore.LIGHTRED_EX + "Failed to update the kill flag on the server. Other users may be affected.")
    except Exception:
        print(Fore.LIGHTRED_EX + "Failed to update the kill flag on the server. Other users may be affected.")

    print(Fore.LIGHTRED_EX + "Quit the game")


def read_chat():
    # Create a temporary file for the screenshot and save it
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    temp_file_path = temp_file.name
    screenshot = ImageGrab.grab()
    screenshot.save(temp_file_path)

    # Run OCR on the image
    img = Image.open(temp_file_path)
    text = pytesseract.image_to_string(img, lang = "eng")

    # Check if the text contains any of the abort strings
    for abort_string in abort_if_in_chat:
        if abort_string in text:
            if override_abort == False:
                abort()

            print(Fore.LIGHTRED_EX + "Found abort string:", abort_string, Fore.LIGHTRED_EX)
            username = getpass.getuser()
            IMAGE_PATH = f"C:\\Users\\{username}\\Desktop\\abort_condition.png"
            screenshot.save(IMAGE_PATH)
            print("Screenshot saved to desktop as abort_condition.png") 

            raise KeyboardInterrupt
     
    #print("temp path:", temp_file_path)
    #print(text)
    temp_file.close()   
    os.remove(temp_file_path) 


def update_status(position):
    global username

    if position == "mining":
        url = app_server_ip + "/client/mining"
    elif position == "stop_mining":
        url = app_server_ip + "/client/stop_mining"

    # Update the usage status on the USA server
    try:
        data = {
            "username": username, 
            "position": position, 
            "version": version,
            "refill_counter": refill_counter
        }  
        response = requests.post(url, json=data)
        if response.status_code == 200:
            #print("Usage status sent successfully.")
            pass
        else:
            print(Fore.LIGHTRED_EX + "Failed to send usage status.")
    except Exception:
        print(Fore.LIGHTRED_EX + "Failed to send usage status to the server.")


def script_updater():
    if update_on_close:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        update_files = [
            "https://raw.githubusercontent.com/besser435/USA-Industries/main/1%20billion%20gecs/client/1_billion_gecs.py",
        ]

        try:
            print("Downloading update...")
            updated_list = []
            for file_name in update_files:
                file_path = os.path.join(script_dir, file_name.split("/")[-1])  # Get the path with file name from the URL
                urllib.request.urlretrieve(file_name, file_path)                # Download file from URL
                
                updated_list.append(file_name.split("/")[-1])                   # Get file name from URL
        except:
            print(Fore.LIGHTRED_EX + "Update download failed. Please manually update files")
        else:
            print("Updated: " + ", ".join(updated_list))


def create_log():
    try:
        url = app_server_ip + "/client/session"
        data = {
            "username": username,
            "version": version,

            "start_time": start_time,
            "end_time": end_time,

            "start_balance": start_balance,
            "end_balance": end_balance,

            "refill_counter": refill_counter,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            #print("Usage status sent successfully.")
            pass
        else:
            print(Fore.LIGHTRED_EX + "Failed to send mining session.")
    except Exception:
        print(Fore.LIGHTRED_EX + "Failed to send mining session to the server.")


def local_backup(data):
    # Backup current data in case the Python script crashes or the server is down
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backup_file = os.path.join(current_dir, "local_backup.txt") # Path to the backup file
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    """
    # Set the maximum number of lines allowed in the file. This is to prevent the file from getting too big
    #max_lines = 32

    # Delete lines if the file exceeds the maximum number of lines   
    with open(backup_file, "r+") as f:
        lines = f.readlines()
        if len(lines) >= max_lines:
            f.seek(0)
            f.truncate()
            f.writelines(lines[-(max_lines - 1):])
    """

    # Write data and timestamp to the backup file
    with open(backup_file, "a") as f:
        f.write(f"{data}    {time}\n")


def main():
    # prepare for autism
    global override_abort
    global start_time
    global refill_counter
    global start_balance
    global end_balance
    global time_stamp
    global end_time

    refill_counter = 0
    try:
        print(f"1 billion gecs {version}")
        unsanitzed_start_balance = input(Fore.LIGHTMAGENTA_EX + "Enter the starting balance: " + Fore.RESET)
        start_balance = float(re.sub("[^0-9.]", "", unsanitzed_start_balance)) # Scrub non-numeric characters
        local_backup(f"start_balance {start_balance}")


        print(f"Starting the money machine in {start_delay} seconds...")
        sleep(start_delay)


        initial_time = time.monotonic()
        last_refill_time = initial_time
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # for json log
        while True: 
            update_status("mining") # Replace with the actual current balance
            current_time = time.monotonic()
            time_stamp = current_time - initial_time + 1    # +1 to not trigger refill_picks() on the first loop
            time_since_refill = current_time - last_refill_time


            pydirectinput.mouseDown()
            mouse.wheel(-1)             # cycle through picks in hotbar
            pydirectinput.press("a")    # timeout prevention. Might cause times to be off by a second occasionally
            pydirectinput.keyDown("tab")


            print(
            "Refill in", int(refill_delay - time_since_refill), "seconds    ",
            "Time elapsed:", round((time_stamp / 3600), 2), "hours    ",
            "Refilled", refill_counter, "times    "
            )
            if override_abort:
                print(Fore.YELLOW + f"WARN: Abort override: {override_abort}")


            # Refill picks after refill_delay seconds
            if time_since_refill >= refill_delay:
                pydirectinput.mouseUp()
                pydirectinput.keyUp("tab")
                refill_picks()
                refill_counter += 1
                last_refill_time = current_time  
            

            # Look for abort strings in chat
            read_chat() 
        

            # Abort if the global kill flag is set to True
            try:
                response = requests.get(app_server_ip + "/killflag")
                kill_flag = response.text
                if kill_flag != "False": 
                    print(Fore.LIGHTRED_EX + "Kill flag set to True")
                    if override_abort == False:
                        abort()
                    raise KeyboardInterrupt
            except Exception:
                print(Fore.LIGHTRED_EX + "Failed to request the kill flag on the server. Will continue, but other users may be affected.")
                pass


            # Keyboard shortcuts
            if keyboard.is_pressed("f7"):   # F7 to stop
                raise KeyboardInterrupt
            pydirectinput.failSafeCheck()   # checks if mouse is in top left corner. If so, raises pydirectinput.FailSafeException and stops everything
          
            if keyboard.is_pressed("f8"):   # F8 to pause
                pydirectinput.mouseUp()
                pydirectinput.keyUp("tab")
                print("Paused. Press F8 to resume")
                time.sleep(1)
                while True:
                    if keyboard.is_pressed("f8"):
                        break
                print("Resumed")

            if keyboard.is_pressed("f9"):   # F9 to refill
                pydirectinput.mouseUp()
                pydirectinput.keyUp("tab")
                refill_picks()
                refill_counter += 1
                last_refill_time = current_time  

            if keyboard.is_pressed("f10"):  # F10 to toggle whether to abort or not
                if override_abort == False:
                    print(Fore.YELLOW + "Enabled abort override. Will not close game when abort is triggered.")
                else:
                    print(Fore.GREEN + "Disabled abort override. Will close game when abort is triggered.")

                override_abort = not override_abort

    except KeyboardInterrupt:
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # for json log
        pydirectinput.mouseUp()
        pydirectinput.keyUp("tab")

        print()
        print("Start balance:", start_balance)
        unsanitzed_end_balance = input(Fore.LIGHTMAGENTA_EX + "Enter the ending balance: " + Fore.RESET)
        end_balance = float(re.sub("[^0-9.]", "", unsanitzed_end_balance)) # Scrub non-numeric characters
        local_backup(f"end_balance {end_balance}")

        print("Done Mining")
        print("Money made: $" + str("{:,.0f}".format(end_balance - start_balance)))
        print("Money per hour: $" + str("{:,.0f}".format((end_balance - start_balance) / (time_stamp / 3600))))
        print("Time elapsed:", round((time_stamp / 3600), 2), "hours")
        print("Refilled picks", refill_counter, "times")
        print("Software version:", version)

        print()
        update_status("stop_mining") # Replace with the actual current balance
        create_log()
        script_updater()
        print()
        
        input("Press enter to exit...")

    except Exception as e:
        print(Fore.LIGHTRED_EX + traceback.format_exc())
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # for json log
        pydirectinput.mouseUp()
        pydirectinput.keyUp("tab")

        print("Start balance:", start_balance)
        unsanitzed_end_balance = input(Fore.LIGHTMAGENTA_EX + "Enter the ending balance: " + Fore.RESET)
        end_balance = float(re.sub("[^0-9.]", "", unsanitzed_end_balance)) # Scrub non-numeric characters
        local_backup(f"end_balance {end_balance}")
        print()

        update_status("stop_mining") # Replace with the actual current balance
        create_log()
        script_updater()
        print()
        
        input("Press enter to exit...")
main()

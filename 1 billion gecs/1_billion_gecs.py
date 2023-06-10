import time, pydirectinput, mouse, keyboard, pytesseract, tempfile, os, getpass#,pyautogui
import usa_secrets, requests
from colorama import init
init()
from colorama import Fore
init(autoreset=True)
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter
from time import sleep
# https://learncodebygaming.com/blog/pyautogui-not-working-use-directinput

# time in seconds before pick refill. 4200 seems to be right for Unbreaking III
REFILL_DELAY = 4200
app_server_ip = usa_secrets.app_server_ip
abort_if_in_chat = usa_secrets.abort_if_in_chat
override_abort = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


version = "1 billion gecs v1.3-beta.2"
#TODO add decoy chat messages and random DC delay

def refill_picks():
    # move to the dohickey
    pydirectinput.keyDown("s")
    sleep(2)
    pydirectinput.keyUp("s")
    pydirectinput.keyDown("d")
    sleep(3)
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
            print(Fore.LIGHTRED_EX + "Failed to update the kill flag on server. Other users may be affected.")
    except Exception:
        print(Fore.LIGHTRED_EX + "Failed to update the kill flag on server. Other users may be affected.")

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


def main():
    global override_abort
    refill_counter = 0
    try:
        print("Starting the money machine in 3 seconds...")
        sleep(3)

        initial_time = time.monotonic()
        last_refill_time = initial_time
        while True: 
            current_time = time.monotonic()
            time_stamp = current_time - initial_time + 1    # +1 to not trigger refill_picks() on the first loop
            time_since_refill = current_time - last_refill_time

            pydirectinput.mouseDown()
            mouse.wheel(-1)             # cycle through picks in hotbar
            pydirectinput.press("a")    # timeout prevention. Might cause times to be off by a second occasionally
            pydirectinput.keyDown("tab")

            print(
            "Refill in", int(REFILL_DELAY - time_since_refill), "seconds    ",
            "Time elsapsed:", round((time_stamp / 3600), 2), "hours    ",
            "Refilled", refill_counter, "times    "
            )

            #sleep(1)

            # if 4000, refills picks every 1.11 hours (about the time a pick lasts)
            if time_since_refill >= REFILL_DELAY:
                pydirectinput.mouseUp()
                pydirectinput.keyUp("tab")
                refill_picks()
                refill_counter += 1
                last_refill_time = current_time  
            
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
                print(Fore.LIGHTRED_EX + "Error connecting to USA Industries server. Will continue, but other users may be affected.")
                pass


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

            if keyboard.is_pressed("f10"):   # F10 to togggle whether to abort or not
                if override_abort == False:
                    print(Fore.YELLOW + "Enabled abort override. Will not close game when abort is triggered.")
                else:
                    print(Fore.GREEN + "Disabled abort override. Will close game when abort is triggered.")

                override_abort = not override_abort

            if override_abort:
                print(Fore.YELLOW + f"WARN: Override abort: {override_abort}")
    

    except KeyboardInterrupt:
        pydirectinput.mouseUp()
        pydirectinput.keyUp("tab")

        print("Done Mining")
        print("Software version:", version)
        print("Time elapsed:", round((time_stamp / 3600), 2), "hours")
        print("Refilled picks", refill_counter, "times")
        input("\nPress enter to exit...")

    except Exception as e:
        print("Error:", e)
        input("\nPress enter to exit...")
main()

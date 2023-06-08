import time, pydirectinput, mouse, keyboard, pytesseract, tempfile, os, getpass#,pyautogui
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter
from time import sleep
# https://learncodebygaming.com/blog/pyautogui-not-working-use-directinput

# time in seconds before pick refill. 4400 seems to be right for Unbreaking III
REFILL_DELAY = 4200
abort_if_in_chat = ["Thenoobcraft74","ADMIN"]
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


version = "1 Billion gecs v1.2"


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
            pydirectinput.mouseUp()
            pydirectinput.keyDown("alt")
            pydirectinput.press("f4")       
            pydirectinput.keyUp("alt")

            print("Found abort string:", abort_string)

            username = getpass.getuser()
            IMAGE_PATH = f"C:\\Users\\{username}\\Desktop\\abort_condition.png"
            screenshot.save(IMAGE_PATH)
            print("Screenshot saved to desktop as abort_condition.png")

            temp_file.close()   
            os.remove(temp_file_path) 

            raise KeyboardInterrupt
    #print("temp path:", temp_file_path)
    #print(text)
    temp_file.close()   
    os.remove(temp_file_path) 


def main():
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
                print("Refilled")
            
            # Don't really want admins finding out about this and nerfing the jobs.
            # This will DC the player if an admin joins the game so they are less likely to find the machine
            read_chat() 
        
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
                print("Refilled")
    

    except KeyboardInterrupt:
        pydirectinput.mouseUp()
        pydirectinput.keyUp("tab")

        print("Done Mining")
        print("Time elapsed:", round((time_stamp / 3600), 2), "hours")
        print("Refilled picks", refill_counter, "times")
        input("\nPress enter to exit...")

    except Exception as e:
        print("Error:", e)
        input("\nPress enter to exit...")
main()

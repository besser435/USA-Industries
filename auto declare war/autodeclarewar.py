import time
import pydirectinput
import mouse
import keyboard
import pytesseract
import tempfile
import getpass
import os 
from colorama import init
init()
from colorama import Fore
init(autoreset=True)
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter
from time import sleep
# https://learncodebygaming.com/blog/pyautogui-not-working-use-directinput

#Will autodeclare war if name is seen on screen. Use some fragments of the name in case OCR is inaccurate
trigger_if_in_chat = ["example1", "example2", "example3"]
override_abort = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def trigger():
    pydirectinput.keyUp("tab")

    #Write war declaration command here
    #Replace {wartype} and {args} with the wartype and town/nation name I guess, it's not rocket science (not like rocket science is actually that hard)
    pydirectinput.write("/declare war {wartype} {args}", interval=0.05)


def read_chat():
    # Create a temporary file for the screenshot and save it
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    temp_file_path = temp_file.name
    screenshot = ImageGrab.grab()
    screenshot.save(temp_file_path)

    # Run OCR on the image
    img = Image.open(temp_file_path)
    text = pytesseract.image_to_string(img, lang = "eng")

    # Check if the text contains any of the trigger strings
    for trigger_string in trigger_if_in_chat:
        if trigger_string in text:
            
            trigger()

            print(Fore.LIGHTRED_EX + "Found trigger string:", trigger_string, Fore.LIGHTRED_EX)
            username = getpass.getuser()
            IMAGE_PATH = f"C:\\Users\\{username}\\Desktop\\war_declaration.png"
            screenshot.save(IMAGE_PATH)
            print("Screenshot saved to desktop as war_declaration.png") 
        
            raise KeyboardInterrupt

     

    temp_file.close()   
    os.remove(temp_file_path) 

    while True:
        pydirectinput.keyDown("tab")
        read_chat()
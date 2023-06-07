import time, pydirectinput#, pyautogui
# https://learncodebygaming.com/blog/pyautogui-not-working-use-directinput

times_clicked = 0
start_time = time.time()
try:
    time.sleep(2)
    print("Clicking...")
    while True:
        pydirectinput.press("4") # select wrench in hotbar

        pydirectinput.keyDown("shift") # dupe XP
        pydirectinput.click(button="right")
        pydirectinput.keyUp("shift")

        pydirectinput.press("9") # select XP in heotbar
        pydirectinput.click(button="right") # use XP

        pydirectinput.press("t")
        pydirectinput.press("esc")


        times_clicked += 1
        #time.sleep(0.1) 

except KeyboardInterrupt:
    end_time = time.time()
    print("Done clicking")
    print("Clicked " + str(times_clicked) + " times")
    print("Time elapsed:", (end_time - start_time) / 3600, "hours")
    input("\nPress enter to exit...")

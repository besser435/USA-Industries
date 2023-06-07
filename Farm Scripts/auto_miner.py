import time, pydirectinput#, pyautogui
# https://learncodebygaming.com/blog/pyautogui-not-working-use-directinput

times_clicked = 0
money_lost = 0
start_time = time.time()
try:
    time.sleep(2)
    print("Clicking...")
    while True:
        pydirectinput.mouseDown()
        time.sleep(0.3) # enough time for the block to be mined (Eff V, Haste II)
        pydirectinput.mouseUp()
        # allows the player to carry two tools for increased farm time by switching tools in offhand
        pydirectinput.press("f") 
        
        time.sleep(2) # jobs plugin cooldown delay
        times_clicked += 1
        money_lost += 5.15

        pydirectinput.press("t")
        pydirectinput.press("esc")
        
except KeyboardInterrupt:
    end_time = time.time()
    print("Done clicking")
    print("Money lost:", money_lost)
    print("Clicked " + str(times_clicked) + " times")
    print("Time elapsed:", (end_time - start_time) / 3600, "hours")
    input("\nPress enter to exit...")

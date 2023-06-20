import requests
import requests
import json
from datetime import datetime
import time
"""
# Update kill flag
url = "http://72.200.111.73:5000/killflag"
new_kill_flag = False 
data = {"kill_flag": new_kill_flag}
response = requests.post(url, json=data)
if response.status_code == 200:
    print("Kill flag updated successfully.")
else:
    print("Failed to update the kill flag.")


# Get kill flag status
response = requests.get("http://72.200.111.73:5000/killflag")
kill_flag = response.text
print(kill_flag)
"""

version = "v1.4"
username = "brandonusa"
refill_counter = 20
app_server_ip = "http://72.200.111.73:5000"

"""def update_status(position):
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
            print("Failed to send usage status.")
    except Exception:
        print("Failed to send usage status to the server.")

    
update_status("mining")
time.sleep(5)
update_status("stop_mining")
"""



start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time.sleep(2)
end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_log():
    try:
        url = app_server_ip + "/client/session"
        data = {
            "username": username,
            "version": version,

            "start_time": start_time,
            "end_time": end_time,

            "start_balance": 0,
            "end_balance": 200,

            "refill_counter": refill_counter,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            #print("Usage status sent successfully.")
            pass
        else:
            print("Failed to send mining session.")
    except Exception:
        print("Failed to send mining session to the server.")

create_log()
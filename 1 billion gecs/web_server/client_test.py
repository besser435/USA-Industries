import requests
import requests
import json
from datetime import datetime
import time

"""# Update kill flag
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

username = "brandonusa"
app_server_ip = "http://72.200.111.73:5000"

# Function to send usage status to the server
def update_status(position, balance):
    global username

    if position == "start":
        url = app_server_ip + "/client/start"
    elif position == "stop":
        url = app_server_ip + "/client/stop"

    # Update the usage status on the USA server
    data = {"username": username, "balance": balance, "position": position}  
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Usage status sent successfully.")
    else:
        print("Failed to send usage status.")

    """# Example usage
    start_bal = 100     # Replace with the actual current balance
    end_bal = 200       # Replace with the actual current balance
    update_status("start", start_bal)
    update_status("stop", end_bal)"""
    
update_status("start", 100)






# Function to start a mining session
def start_mining_session(initial_money):
    global start_time
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_data = {
        "username": username,
        "start_time": start_time,
        "initial_money": initial_money
    }
    response = requests.post(app_server_ip + "/start_session", json=session_data)
    if response.status_code == 200:
        print("Mining session started successfully.")
    else:
        print("Failed to start mining session.")

# Function to stop a mining session
def stop_mining_session(final_money):
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_data = {
        "username": username,
        "start_time": start_time,
        "end_time": end_time,
        "final_money": final_money
    }
    response = requests.post(app_server_ip + "/stop_session", json=session_data)
    if response.status_code == 200:
        print("Mining session stopped successfully.")
    else:
        print("Failed to stop mining session.")

# Example usage
start_mining_session(1000)
time.sleep(1)
# Perform mining operations...
stop_mining_session(1200)

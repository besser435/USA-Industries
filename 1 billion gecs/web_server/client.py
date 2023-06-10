import requests

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

username = "brandonusa"
server = "http://72.200.111.73:5000/"

# Function to send usage status to the server
def send_usage_status_start(url, username, start_bal):
    data = {"username": username, "start_bal": start_bal}  
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Usage status sent successfully.")
    else:
        print("Failed to send usage status.")

# Example usage
start_bal = 100     # Replace with the actual current balance
send_usage_status_start(server + "/client/start", username, start_bal)

"""
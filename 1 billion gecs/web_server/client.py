import requests

url = "http://192.168.0.157:5000/killflag"
new_kill_flag = False  

data = {"kill_flag": new_kill_flag}
response = requests.post(url, json=data)

if response.status_code == 200:
    print("Kill flag updated successfully.")
else:
    print("Failed to update the kill flag.")



import requests
response = requests.get("http://72.200.111.73:5000/killflag")
kill_flag = response.text
print(kill_flag)

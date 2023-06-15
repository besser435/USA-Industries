"""print(
    "brandonusa"s Stats: \n"
    "Currently farming: Yes \n"
    "Current balance: $morbillion \n"
    "Average hourly gain: $220,000 \n"
    "Average daily gain: $2,000,420 \n"
    "Money gained over 24h: $morbtrillion \n"
    "Balance change over 24h: +5% \n"
    "Total time spent mining: 69h 69m \n"    
)

print(
    "\nGeneral info: \n"
    "Total money: $morbillion \n"
    "Average (or mean?) money gain/h: $440,000 \n"
    "Estimated time until $1 billion: 3d \n"
)

print(
    "\nMeta info: \n"
    "Global Kill flag status: False \n"

    "Database size: 69MB \n"
    "Uptime since restart: 1d 13h 3m \n"
)"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os

app = Flask(__name__, static_folder="static")

# Global vars
kill_flag = False
usage_status = {}

# Home page
@app.route("/")
def hello():
    global kill_flag
    global usage_status
    return render_template("home.html", kill_flag=kill_flag, usage_status=usage_status)
# Server options page
@app.route("/options")
def options():  #NOTE changed this name. make sure it still works
    global kill_flag
    global usage_status
    return render_template("options.html", kill_flag=kill_flag)






# Get kill flag status
@app.route("/killflag", methods=["GET"])
def get_kill_flag():
    global kill_flag
    return str(kill_flag)
# Update kill flag status
@app.route("/killflag", methods=["POST"])
def update_kill_flag():
    global kill_flag
    kill_flag = request.json.get("kill_flag")
    return "Kill flag updated successfully."
# Toggle kill flag status from options.html
@app.route("/togglekillflag", methods=["POST"])
def toggle_kill_flag():
    global kill_flag
    kill_flag = not kill_flag
    return redirect(url_for("options"))




# Update farming status
@app.route("/client/start", methods=["POST"])
def start_usage():
    username = request.json.get("username")  # Retrieve the username from the request payload
    start_bal = request.json.get("start_bal")  
    if username:
        # Process the received request to indicate the start of usage for the given username
        # You can update a database, modify a global variable, or perform any required actions
        # based on the specific needs of your application
        # ...
        usage_status[username] = "Currently farming"
        return "Usage status received for username: {}".format(username)
    else:
        return "Username not provided.", 400  # Return an appropriate error response if username is not provided
@app.route("/client/stop", methods=["POST"])
def stop_usage():
    username = request.json.get("username")  # Retrieve the username from the request payload
    end_bal = request.json.get("end_bal")  
    if username:
        # Process the received request to indicate the stop of usage for the given username
        # ...
        usage_status.pop(username, None)
        return "Usage status received for username: {}".format(username)
    else:
        return "Username not provided.", 400  # Return an appropriate error response if username is not provided




# Function to store session data in JSON file
def store_session_data(session_data):
    username = session_data["username"]
    #keyError, this isnt present when stop_mining is called
    start_time = session_data["start_time"] 
    end_time = session_data.get("end_time", "")
    filename = f"{username}_{start_time}_{end_time}_session.json"


    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the subdirectory within the script directory
    subdirectory = "user_sessions"
    directory = os.path.join(script_dir, subdirectory, username)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the session data to a file within the subdirectory
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as file:
        json.dump(session_data, file)



"""
GPT output

def store_session_data(session_data):
    username = session_data["username"]
    filename = f"{username}_session.json"
    with open(filename, "w") as file:
        json.dump(session_data, file)

"""




# Route to start a mining session
@app.route("/start_session", methods=["POST"])
def start_session():
    session_data = request.json
    store_session_data(session_data)
    return jsonify({"message": "Mining session started."}), 200

# Route to stop a mining session
@app.route("/stop_session", methods=["POST"])
def stop_session():
    session_data = request.json
    store_session_data(session_data)
    return jsonify({"message": "Mining session stopped."}), 200




if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")


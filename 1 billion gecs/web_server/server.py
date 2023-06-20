from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import psutil
import datetime 

app = Flask(__name__, static_folder="static")

# Global vars
kill_flag = False
usage_status = {}


"""def update_metadata(username):
    total_money = calculate_total_money(username)
    average_daily_gain = calculate_average_daily_gain(username)
    time_spent_mining = calculate_time_spent_mining(username)
    mining_sessions = calculate_mining_sessions(username)

    metadata = {
        "username": username,
        "total_money": total_money,
        "average_daily_gain": average_daily_gain,
        "time_spent_mining": time_spent_mining,
        "mining_sessions": mining_sessions
    }

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the subdirectory within the script directory
    subdirectory = "user_sessions"
    directory = os.path.join(script_dir, subdirectory, username)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the metadata to a file within the subdirectory
    filepath = os.path.join(directory, "metadata.json")
    with open(filepath, "w") as file:
        json.dump(metadata, file)

    print(f"Metadata updated for user: {username}")"""
def update_all_metadata():
    metadata_dir = "user_sessions"
    
    for root, dirs, files in os.walk(metadata_dir):
        for file in files:
            if file.endswith("metadata.json"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    metadata = json.load(f)
                
                username = metadata["username"]
                metadata_filename = f"{username}_metadata.json"
                metadata_filepath = os.path.join(root, metadata_filename)
                
                # Update the metadata fields as needed
                metadata["total_money"] = calculate_total_money(username)
                metadata["average_daily_gain"] = calculate_average_daily_gain(username)
                metadata["time_spent_mining"] = calculate_time_spent_mining(username)
                metadata["mining_sessions"] = calculate_mining_sessions(username)
                
                with open(metadata_filepath, "w") as f:
                    json.dump(metadata, f, indent=4)
                    
                print(f"Updated metadata file: {metadata_filepath}")


def calculate_total_money(username):
    latest_session_file = get_latest_session_file(username)
    if latest_session_file is None:
        return 0

    filepath = os.path.join("user_sessions", username, latest_session_file)
    with open(filepath) as file:
        data = json.load(file)
        end_balance = data["end_balance"]

    return end_balance


def get_latest_session_file(username):
    directory = os.path.join("user_sessions", username)
    session_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("session.json"):
                session_files.append(file)

    if not session_files:
        return None

    latest_session_file = max(session_files)
    return latest_session_file


def calculate_average_daily_gain(username):
    total_money = calculate_total_money(username)
    time_spent_mining = calculate_time_spent_mining(username)
    days = time_spent_mining / (24 * 60 * 60)  # Convert time spent mining to days
    average_daily_gain = total_money / days
    return average_daily_gain


def calculate_time_spent_mining(username):
    time_spent_mining = 0
    directory = os.path.join("user_sessions", username)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("session.json"):
                filepath = os.path.join(root, file)
                with open(filepath) as f:
                    data = json.load(f)
                    start_time = datetime.datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S")
                    duration = end_time - start_time
                    time_spent_mining += duration.total_seconds()
    return time_spent_mining


def calculate_mining_sessions(username):
    directory = os.path.join("user_sessions", username)
    session_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("session.json"):
                session_count += 1
    return session_count




























def get_total_money():
    total_money = 0
    for root, dirs, files in os.walk("user_sessions"):
        for file in files:
            if file.endswith("metadata.json"):
                filepath = os.path.join(root, file)
                print("reading file:", filepath)
                with open(filepath) as f:
                    data = json.load(f)
                    money = data["total_money"]
                    total_money += money
                    
    formatted_total_money = "{:,}".format(total_money)  # Add commas to total money
    return formatted_total_money
def get_average_daily_money_gain():
    pass
def get_total_time_spent_mining():
    #TODO
    return 1000000
def get_time_until_1_billion():
    #TODO
    return 1000000



# Get "Database" size
# called by
def get_folder_size(folder_path):
    total_size = 0
    for path, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    folder_size_kb = total_size / 1024  # Convert bytes to kilobytes
    return "{:.2f}".format(folder_size_kb) 

def get_server_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = datetime.datetime.now().timestamp() - boot_time
    uptime = datetime.timedelta(seconds=uptime_seconds)
    formatted_uptime = "{}d {}h {}m".format(uptime.days, uptime.seconds // 3600, (uptime.seconds // 60) % 60)
    return formatted_uptime


# Home page
@app.route("/")
def hello():
    global kill_flag
    global usage_status

    folder_size_kb = get_folder_size("user_sessions")
    server_uptime = get_server_uptime()
    total_money  = get_total_money()
    update_all_metadata()

    return render_template(
        "home.html", 
        kill_flag=kill_flag, 
        usage_status=usage_status,
        folder_size_kb=folder_size_kb,
        server_uptime=server_uptime,
        total_money=total_money

    )
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
# called by toggleKillFlag() in options.html
@app.route("/togglekillflag", methods=["POST"])
def toggle_kill_flag():
    global kill_flag
    kill_flag = not kill_flag
    return redirect(url_for("options"))


# Update usage status
# called by update_status() in 1bg.py
@app.route("/client/mining", methods=["POST"])
def start_usage():
    username = request.json.get("username")  # Retrieve the username from the request payload
    version = request.json.get("version")
    refill_counter = request.json.get("refill_counter")
    if username:
        usage_status[username] = {"status": "Currently farming", 
                                  "version": version, 
                                  "refill_counter": refill_counter}
        return "Usage status received for username: {} (version {})".format(username, version)
    else:
        return "Username not provided.", 400  # Return an appropriate error response if username is not provided
@app.route("/client/stop_mining", methods=["POST"])
def stop_usage():
    username = request.json.get("username")  # Retrieve the username from the request payload
    if username:
        usage_status.pop(username, None)
        return "Usage status received for username: {}".format(username)
    else:
        return "Username not provided.", 400  # Return an appropriate error response if username is not provided




# Function to store session data in JSON file
# called by create_log() in 1bg.py
@app.route("/client/session", methods=["POST"])
def store_session_data():
    print("Storing session data...")
    session_data = request.json
    username = session_data["username"]
    start_time = session_data["start_time"] 
    end_time = session_data["end_time"] 
    filename = f"{username}_{start_time}___{end_time}_session.json"

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the subdirectory within the script directory
    subdirectory = "user_sessions"
    directory = os.path.join(script_dir, subdirectory, username)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Created directory:", directory)

    # Write the session data to a file within the subdirectory
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as file:
        json.dump(session_data, file)
        print(f"Mining session stored successfully for {username}.")

    return f"Mining session stored successfully for {username}."

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")


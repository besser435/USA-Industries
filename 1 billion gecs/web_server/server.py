"""print(
    "brandonusa"s Stats: \n"
    "Currently farming: Yes \n"
    "Current balance: $morbillion \n"
    "Average hourly gain: $220,000 \n"
    "Average daily gain: $2,000,420 \n"
    "Money gained over 24h: $morbtrillion \n"
    "Balance change over 24h: +5% \n"
    "Leaderboard position: 1 \n"
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

    "Data received 1.69MB (last 24h): \n"
    "Data sent (last 24h): 0.42MB \n"

    "Data received 1.69MB (all-time): 90MB\n"
    "Data sent 0.42MB (all-time): 53MB\n"

    "Total data transferred (all-time): 0.42MB \n"
    "Total data transferred (all-time): 0.42MB \n"

    "Database size: 69MB \n"
    "Uptime since restart: 1d 13h 3m \n"
)"""

from flask import Flask, request

app = Flask(__name__)

# Global kill flag variable
kill_flag = False

@app.route("/")
def hello():
    return "Homepage"

@app.route("/killflag", methods=["GET"])
def get_kill_flag():
    global kill_flag
    return str(kill_flag)

@app.route("/killflag", methods=["POST"])
def update_kill_flag():
    global kill_flag
    kill_flag = request.json.get("kill_flag")
    return "Kill flag updated successfully."

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")


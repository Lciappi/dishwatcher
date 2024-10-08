from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS configuration
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")  # SocketIO CORS configuration

@app.route('/')
def index():
    return jsonify({"status": "OK"})

# always sends ALL data, assume nothing is persisted in the front end

@app.route("/calibrate", methods=['POST'])
def calibrate_sink():
    # calibrate(frame_queue=frame_queue)
    return jsonify({"status": "Calibration complete"})

# fetch the initial activity state
@app.route("/activity", methods=['GET'])
def send_activity_to_client():
    message = [
        {
            user: 'Leo Ciappi',
            action: 'cleaned',
            time: '09:30 am',
            color: 'primary',
            variant: 'outlined',
        },
        {
            user: 'Yeojun Han',
            action: 'contaiminated',
            time: '09:40 am',
            color: 'warning',
            variant: 'outlined',
        },
        {
            user: 'Yeojun Han',
            action: 'cleaned',
            time: '09:43 am',
            color: 'primary',
            variant: 'outlined',
        },
        {
            user: 'Leo Ciappi',
            action: 'contaminated',
            time: '09:50 am',
            color: 'warning',
            variant: 'outlined',
        },
    ]
    socketio.emit('activity', message)
    return jsonify({"activity": message})

# logs ordered by who is doing what, independent by time
# for the dashboard and leaderboard
# per user grouping
@app.route("/log", methods=['GET'])
def send_log_to_client():
    message = [ # dummy data
        {
            id: 1,
            name: "Leo Ciappi",
            logs: [
                {
                    id: "event",
                    image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                    time: "1:32 PM",
                    event: "Cleaned"
                },
                {
                    id: "event",
                    image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                    time: "2:00 AM",
                    event: "Contaminated"
                },
            ],
        },
        {
            id: 2,
            name: "Yeojun Han",
            logs: [
                {
                    id: "event",
                    image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                    time: "1:54 AM",
                    event: "Contaminated"
                },
            ],
        }
    ]
    socketio.emit('log', message)
    return jsonify({"log": message})

# notifications for given user
@app.route("/notifications/", methods=['GET'])
def send_notifications_to_client(username, action):
    message = {
        user: username,
        action: action
    }

    socketio.emit('notifications', message)
    return jsonify({"notifications": message})

def main():
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from face_recognition import recognize

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS configuration
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")  # SocketIO CORS configuration

@app.route('/')
def index():
    return jsonify({"status": "OK"})

@app.route("/hello", methods=['GET'])
def send_message_to_client():
    socketio.emit('hello', "Hello from the server!")
    return jsonify({"hello": "Hello from the server!"})

@app.route("/sink", methods=['GET'])
def send_sink_to_client(): 
    socketio.emit('sink', 'insert image url here hehe')
    return jsonify({"sink": "insert image url here hehe"})

@app.route("/offender", methods=['GET'])
def send_offender_to_client():
    socketio.emit('offender', 'insert picture of new offender here')
    return jsonify({"offender": "insert picture of new offender here"})

@app.route("/offenders", methods=['GET'])
def send_offenders_to_client():
    socketio.emit('offenders', 'insert pictures of offenders here')
    return jsonify({"offenders": "insert pictures of offenders here"})

@app.route("/notification", methods=['GET'])
def send_notification_to_client():
    socketio.emit('notification', 'insert new notification here')
    return jsonify({"notification": "insert new notification here"})

@app.route("/notifications", methods=['GET'])
def send_notifications_to_client():
    socketio.emit('notifications', 'insert list of notifications here')
    return jsonify({"notifications": "insert list of notifications here"})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
    recognize()
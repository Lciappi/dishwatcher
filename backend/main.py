from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

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


# Load pre-trained face detection model
# model_path = os.getenv('MODEL_PATH', 'haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + model_path)

# Initialize video capture
# video_capture = cv2.VideoCapture(0)

# @app.route('/current_image', methods=['GET'])
# def get_current_image():
#     ret, frame = video_capture.read()
#     if not ret:
#         return jsonify({'error': 'Could not read from camera'}), 500
#     _, buffer = cv2.imencode('.jpg', frame)
#     return Response(buffer.tobytes(), mimetype='image/jpeg')

# @app.route('/detect_faces', methods=['GET'])
# def detect_faces():
#     ret, frame = video_capture.read()
#     if not ret:
#         return jsonify({'error': 'Could not read from camera'}), 500
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#     face_list = [{'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)} for (x, y, w, h) in faces]
#     return jsonify({'faces': face_list})
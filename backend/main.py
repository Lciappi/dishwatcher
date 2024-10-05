import os
import cv2
from flask import Flask, jsonify, Response

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

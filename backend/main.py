from queue import Queue
import threading
import face_recognition
import cv2
import numpy as np
from queue import Queue
from datetime import datetime
import random
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import time


'''
    ================================================================================
    ENDPOINTS                                                                     ||
    ================================================================================
'''

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS configuration [allow frontend]
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")  # SocketIO CORS configuration
frame_queue = Queue()

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
def send_activity_to_client(activity):
    print("Sending activity to frontend")
    print("activity:", activity)
    print("=====================================")
    socketio.emit('activity', activity)
    return jsonify({"activity": activity})

# logs ordered by who is doing what, independent by time
# for the dashboard and leaderboard
# per user grouping
@app.route("/log", methods=['GET'])
def send_log_to_client(log):
    print("Sending log to frontend")
    print("log_flask: ", log)
    socketio.emit('log', log)
    return jsonify({"log": log})

# notifications for given user
@app.route("/notifications/", methods=['GET'])
def send_notifications_to_client(username, action):
    message = {
        'user': username,
        'action': action
    }

    socketio.emit('notifications', message)
    return jsonify({'notifications': message})

# reference: https://github.com/ageitgey/face_recognition
'''
    ================================================================================
    Events
    ================================================================================

    These functions are used when the AI detects an event that needs to be reported 
    to the frontend.

    user added plates():
        This means a user added a plate
        We need to update the activity panel
        We need to update the per-user log panel

    user_cleaned_plates():
        update activity panel
        update logs
'''

activity = []

'''
    LOG DICTIONARY
    log[user] = {
        'id': int,
        'name': str,
        'logs':
            [
                {
                    'id': random_integer,
                    'image': "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                    'time': curr_time,
                    'event': "Contaminated",
                }
            ]

    }
'''
log = {}

def maybe_initialize_user(user: str):
    print("maybe_initialize_user")
    if user not in log:
        log[user] = {
            'id': len(activity),
            'name': user,
            'logs': [],
        }


'''
    Gets the user plates

    #TODO: YJ how the fuck are we going to sent an image of the culprit?
            is it too much of a nice to have?
'''
def user_added_plates(user: str, image: str, cleaned: bool):
    # Send notification
    print("Sending notification [user_added_plates] to frontend")
    curr_time = datetime.now().strftime('%I:%M:%S %p')

    send_notifications_to_client(user, " added plates to the sink")

    # Send dashboard - activity
    print("Sending activity [user_added_plates] to frontend")

    new_item = {
        'user': user,
        'action': 'cleaned' if cleaned else 'contaminated',
        'time': curr_time,
        'color': 'warning',
        'variant': 'outlined',
    }

    activity.append(new_item)
    send_activity_to_client(activity[::-1])

    # Send dashboard - log
    print("Sending log [user_added_plates] to frontend")
    maybe_initialize_user(user)
    random_integer = random.randint(1, 10000)

    # TODO: Add image to log object

    new_log = {
        'id': random_integer,
        'image': "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
        'time': curr_time,
        'event': "Cleaned" if cleaned else "Contaminated",
    }

    log[user]['logs'].append(new_log)

    print("\n\n ============= logic base log: \n", log.values())
    print("converting")
    list_log = []
    for key in log.keys():
        list_log.append(log[key])

    # must reverse activity to show the latest event first
    send_log_to_client(list_log[::-1])

person_in_frame = None
dish_in_sink = False

retrieve_frame = False


def recognize_faces(frame_queue: Queue):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    leo_image = face_recognition.load_image_file("images/leo.jpg")
    leo_face_encoding = face_recognition.face_encodings(leo_image)[0]

    # Load a second sample picture and learn how to recognize it.
    yeojun_image = face_recognition.load_image_file("images/yeojun.jpg")
    yeojun_face_encoding = face_recognition.face_encodings(yeojun_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        leo_face_encoding,
        yeojun_face_encoding
    ]
    known_face_names = [
        "Leo Ciappi",
        "Yeojun Han"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # print name if person appears in the frame for the first time or leaves the frame
        global person_in_frame
        if len(face_names) > 0 and person_in_frame != face_names[0]:
            person_in_frame = face_names[0]
            print("SENDING NOTIFICATION", person_in_frame)
            app.app_context().push()
            if person_in_frame != "Unknown":
                send_notifications_to_client(person_in_frame, "entered the frame")
            print(person_in_frame)
        elif len(face_names) == 0 and person_in_frame != None:
            person_in_frame = None
            print("Person left")

        # print if a dish is added or removed from the frame
        person_holding_dish = False
        global dish_in_sink
        if person_holding_dish and not dish_in_sink:
            dish_in_sink = True
            print("Dish added for the first time")
        elif person_holding_dish and dish_in_sink:
            print("More dish added to sink")
        elif not person_holding_dish and dish_in_sink:
            dish_in_sink = False
            print("Person walking by")

        # Put the frame into the queue
        global retrieve_frame
        if retrieve_frame:
            retrieve_frame = False
            frame_queue.put(frame)

        # Display the results
        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4

        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #     # Draw a label with a name below the face
        #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # # Display the resulting image
        # cv2.imshow('Video', frame)

        # # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release handle to the webcam
    video_capture.release()
    # cv2.destroyAllWindows()


def calibrate(frame_queue: Queue):
    # set global retrieve_frame to true
    global retrieve_frame
    retrieve_frame = True

    # get the frame from the queue
    curr_frame = frame_queue.get(block=True, timeout=10)

    print(curr_frame.shape)

    # Perform calibration using the frame
    # (Add your calibration logic here)

    # Display the frame (for debugging purposes)
    # cv2.imshow('Calibration', frame)

    # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


'''
    ================================================================================
    INTEGRATION TESTS
    ================================================================================
'''

def test_contaminated_sink():
    app.app_context().push()
    print("Started test thread")
    time.sleep(5)
    print("10 second countdown")
    time.sleep(5)
    print("5 second countdown")
    time.sleep(5)
    print("Testing contaminated sink")
    user_added_plates("Leo Ciappi", "https://cdn.pixabay.com/photo/2016/03/31/19/30/dish-1295066_640.png", True)
    time.sleep(5)
    user_added_plates("Yeojun Han", "https://cdn.pixabay.com/photo/2016/03/31/19/30/dish-1295066_640.png", False)
    time.sleep(5)
    user_added_plates("Leo Ciappi", "https://cdn.pixabay.com/photo/2016/03/31/19/30/dish-1295066_640.png", False)
    time.sleep(5)
    print("Test ended")

if __name__ == '__main__':
    # threading.Thread(target=recognize_faces, args=(frame_queue,), daemon=True).start()
    threading.Thread(target=test_contaminated_sink, daemon=True).start()
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')

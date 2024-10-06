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
from ultralytics import YOLO
from io import BytesIO
import time
from PIL import Image
import base64

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

@app.route('/offender', methods=['GET'])
def get_offender():
    # Process the image (e.g., resize, convert to base64)
    img = frame_queue.get(True, 10)
    img_bytes = BytesIO()
    image_data = img_bytes.getvalue().decode('base64')

    # Emit the image data to the frontend
    socketio.emit('image', {'image_data': image_data})

    return jsonify({'message': 'Image uploaded successfully'})

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
    print("Sending log [user_added_plates] to frontend") # TODO: the program dies after this line
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
    existing_object_counts = {}
    person_in_frame = None

    process_this_frame = True

    # Load a pretrained YOLO11n model
    model = YOLO("yolo11n.pt")

    dish_in_sink = False
    prev_dish_in_sink = False
    prev_object_count = 0
    buffer_size = 5
    object_buffer = {
        "bowl": [],
        "cup": [],
        "fork": [],
        "knife": [],
        "spoon": [],
        "bottle": [],
        "wine glass": [],
        "scissors": []
    }

    # Load a pretrained YOLO11n model
    model = YOLO("yolo11n.pt")

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Only process every other frame of video to save time
        if process_this_frame:
            '''
            ================================================================
            ||                                                            ||
            ||                      Frame processing                      ||
            ||                                                            ||           
            ================================================================
            '''
            '''
            ================================================================
            ||                                                            ||
            ||                      Frame processing                      ||
            ||                                                            ||           
            ================================================================
            '''
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # split frame into two halves (top and bottom)
            height, width, channels = small_frame.shape
            midpoint = height // 2

            # Split the image vertically
            # top_half = small_frame[:midpoint, :]
            small_frame_bottom = small_frame[midpoint:, :]

            # print(f"Top half shape: {top_half.shape}")
            # print(f"Bottom half shape: {small_frame_bottom.shape}")

            # split frame into two halves (top and bottom)
            height, width, channels = small_frame.shape
            midpoint = height // 2

            # Split the image vertically
            # top_half = small_frame[:midpoint, :]
            small_frame_bottom = small_frame[midpoint:, :]

            # print(f"Top half shape: {top_half.shape}")
            # print(f"Bottom half shape: {small_frame_bottom.shape}")

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            rgb_small_frame_bottom = np.ascontiguousarray(small_frame_bottom[:, :, ::-1])

            '''
            ================================================================
            ||                                                            ||
            ||                     Facial Recognition                     ||
            ||                                                            ||           
            ================================================================
            '''
            rgb_small_frame_bottom = np.ascontiguousarray(small_frame_bottom[:, :, ::-1])

            '''
            ================================================================
            ||                                                            ||
            ||                     Facial Recognition                     ||
            ||                                                            ||           
            ================================================================
            '''
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

            '''
            ================================================================
            ||                                                            ||
            ||                      Dish Recognition                      ||
            ||                                                            ||           
            ================================================================
            '''
            # Run inference on the source
            classes = [
                # 0,  # person
                39, # bottle
                40, # wine glass
                41, # cup
                42, # fork
                43, # knife
                44, # spoon
                45, # bowl
                # 71, # sink
                76, # scissors
            ]

            results = model.predict(rgb_small_frame_bottom, verbose=False, classes=classes)

            # Initialize a dictionary to count occurrences of each class
            object_counts = {}

            # Iterate over the results generator
            for result in results:
                
                # Get the class names
                names = result.names  
                
                # Iterate through detected boxes
                for detection in result.boxes:
                    label = names[int(detection.cls)]  # Get the label using the class index
                    
                    # Count occurrences of each label
                    if label in object_counts:
                        object_counts[label] += 1
                    else:
                        object_counts[label] = 1
            
            # -- object buffer logic here --
            any_object_detected = False
            all_objects_below_threshold = True

            # update object detection buffer
            for obj in object_buffer.keys():
                if obj in object_counts:
                    object_buffer[obj].append(object_counts[obj])
                else:
                    object_buffer[obj].append(0)  # No object detected

                # Maintain buffer size
                if len(object_buffer[obj]) > buffer_size:
                    object_buffer[obj].pop(0)

                # Calculate the average for the current object
                if len(object_buffer[obj]) > 0:  # Ensure there are values to average
                    average_count = np.average(object_buffer[obj])
                    
                    # Check if object was seen more than half the times
                    if average_count > 0.5:
                        any_object_detected = True
                    else: 
                        all_objects_below_threshold = all_objects_below_threshold and True
                else: 
                    all_objects_below_threshold = False

            # Set dish_in_sink based on the flags
            prev_dish_in_sink = dish_in_sink
            if any_object_detected:
                dish_in_sink = True
            elif all_objects_below_threshold:
                dish_in_sink = False

            # # Print the counts of each object
            # for label, count in object_counts.items():
            #     print(f"{label}: {count}")

            # Additional logic to handle dish_in_sink state
            if dish_in_sink != prev_dish_in_sink:
                current_object_count = sum(object_counts.values())
            
                if dish_in_sink:
                    # object count increased (added object)
                    if person_in_frame and current_object_count > prev_object_count: 
                        print(person_in_frame, "ADDED plates")
                        frame_queue.put(frame)
                        get_offender()
                        # user_added_plates(person_in_frame, "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg")
                    print("Dish is in the sink.")
                else:
                    # object count increased (cleaned)
                    if person_in_frame and current_object_count == 0 and prev_object_count > 0: 
                        print(person_in_frame, "CLEANED plates")
                        frame_queue.put(frame)
                        get_offender()
                        # user_cleaned_plates(person_in_frame)
                    print("No dish in the sink.")

                prev_object_count = current_object_count


        process_this_frame = not process_this_frame

        # print name if person appears in the frame for the first time or leaves the frame
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

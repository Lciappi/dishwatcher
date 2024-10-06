import face_recognition
import cv2
import numpy as np
from queue import Queue
from datetime import datetime
import random

#from main import send_notifications_to_client, send_activity_to_client

# reference: https://github.com/ageitgey/face_recognition

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
    Events
    ================================================================================
    
    These functions are used when the AI detects an event that needs to be reported 
    to the frontend.
    
    user_added_plates():
        This means a user added a plate
        We need to update the activity panel
        We need to update the per-user log panel
        
    user_cleaned_plates():
        update activity panel
        update logs
'''


activity = []
log = []

def maybe_initialize_user(user: str):
    for user in activity:
        if user.get('name') == user:
            return
        else:
            new_user = {
                id: len(activity),
                name: user,
                logs: [],
            }
            activity.append(new_user)


'''
    Gets the user plates
    
    #TODO: YJ how the fuck are we going to sent an image of the culprit?
            is it too much of a nice to have?
'''
def user_added_plates(user: str, image: str):
    # Send notification
    print("Sending notification [user_added_plates] to frontend")
    curr_time = datetime.now().strftime('%I:%M %p')

    # send_notifications_to_client(user, " added plates to the sink")

    # Send dashboard - activity
    print("Sending activity [user_added_plates] to frontend")

    new_item = {
        user: 'Leo Ciappi',
        action: 'contaminated',
        time: curr_time,
        color: 'warning',
        variant: 'outlined',
    }

    activity.append(new_item)
    # send_activity_to_client(activity)

    # Send dashboard - log
    print("Sending log [user_added_plates] to frontend")
    maybe_initialize_user(user)
    random_integer = random.randint(1, 10000)

    #TODO: Add image to log object

    new_log = {
        id: random_integer,
        image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
        time: curr_time,
        event: "Contaminated",
    }

    for user in activity:
        if user.get('name') == user:
            user['logs'].insert(0, new_log)

    # send_activity_to_client(activity)

def user_cleaned_plates(user: str):
    # Send dashboard - log
    # Send dashboard - activity
    # Send notification
    print("Sending user_cleaned_plates to frontend")


from flask import jsonify
import face_recognition
import cv2
import numpy as np
from queue import Queue

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
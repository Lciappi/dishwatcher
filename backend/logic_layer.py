import time
import threading
from event_bus import EventBus
import cv2
import face_recognition
import numpy as np
from queue import Queue
from ultralytics import YOLO

class LogicLayer(threading.Thread):
    def __init__(self, event_bus):
        super().__init__()
        self.event_bus = event_bus
        self.whatever = 0
        self.frame_queue = Queue()
        self.person_in_frame = None
        self.dish_in_sink = False
        self.last_action = None
        self.process_this_frame = True
        self.prev_dish_in_sink = False
        self.prev_object_count = 0
        self.buffer_size = 5
        self.object_buffer = {
            "bowl": [],
            "cup": [],
            "fork": [],
            "knife": [],
            "spoon": [],
            "bottle": [],
            "wine glass": [],
            "scissors": []
        }
        self.video_capture = cv2.VideoCapture(0)

        # Load the face encodings
        leo_image = face_recognition.load_image_file("images/leo.jpg")
        self.leo_face_encoding = face_recognition.face_encodings(leo_image)[0]
        yeojun_image = face_recognition.load_image_file("images/yeojun.jpg")
        self.yeojun_face_encoding = face_recognition.face_encodings(yeojun_image)[0]
        self.known_face_encodings = [self.leo_face_encoding, self.yeojun_face_encoding]
        self.known_face_names = ["Leo Ciappi", "Yeojun Han"]

        # Load the pretrained YOLO model
        self.model = YOLO("yolo11n.pt")

    def recognize_faces_and_objects(self):
        ret, frame = self.video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            return None

        if self.process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            height, width, channels = small_frame.shape
            midpoint = height // 2
            small_frame_bottom = small_frame[midpoint:, :]
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            rgb_small_frame_bottom = np.ascontiguousarray(small_frame_bottom[:, :, ::-1])

            # Facial recognition
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    face_names.append(name)

            # Object recognition
            classes = [39, 40, 41, 42, 43, 44, 45, 76]
            results = self.model.predict(rgb_small_frame_bottom, verbose=False, classes=classes)
            object_counts = {}
            for result in results:
                names = result.names
                for detection in result.boxes:
                    label = names[int(detection.cls)]
                    if label in object_counts:
                        object_counts[label] += 1
                    else:
                        object_counts[label] = 1

            # Buffer logic
            any_object_detected = False
            all_objects_below_threshold = True
            for obj in self.object_buffer.keys():
                if obj in object_counts:
                    self.object_buffer[obj].append(object_counts[obj])
                else:
                    self.object_buffer[obj].append(0)

                if len(self.object_buffer[obj]) > self.buffer_size:
                    self.object_buffer[obj].pop(0)

                if np.average(self.object_buffer[obj]) > 0.5:
                    any_object_detected = True
                else:
                    all_objects_below_threshold = all_objects_below_threshold and True

            # Dish recognition state update
            self.prev_dish_in_sink = self.dish_in_sink
            if any_object_detected:
                self.dish_in_sink = True
            elif all_objects_below_threshold:
                self.dish_in_sink = False

            current_object_count = sum(object_counts.values())
            if self.dish_in_sink != self.prev_dish_in_sink:
                if self.dish_in_sink:
                    if self.person_in_frame and current_object_count > self.prev_object_count:
                        if self.last_action != "contaminated":
                            self.frame_queue.put(frame)
                            self.event_bus.publish({"type": "contaminated", "user": self.person_in_frame, "message": "added plates"})
                            self.last_action = "contaminated"
                else:
                    if self.person_in_frame and current_object_count == 0 and self.prev_object_count > 0:
                        if self.last_action != "cleaned":
                            self.frame_queue.put(frame)
                            self.event_bus.publish({"type": "cleaned", "user": self.person_in_frame, "message": "cleaned plates"})
                            self.last_action = "cleaned"

                self.prev_object_count = current_object_count

            if len(face_names) > 0 and self.person_in_frame != face_names[0]:
                self.person_in_frame = face_names[0]
                self.event_bus.publish({"type": "suspect_frame", "user": self.person_in_frame, "message": "entered the frame"})
            elif len(face_names) == 0 and self.person_in_frame is not None:
                self.person_in_frame = None
                print("Person left")

        self.process_this_frame = not self.process_this_frame

    def run(self):
        print("Layer B (AI model) started")
        while True:
            time.sleep(8)  # Simulate time gap between frame processing
            self.recognize_faces_and_objects()

        self.video_capture.release()

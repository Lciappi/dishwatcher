import threading
import random
from datetime import datetime

class IntegrationLayer(threading.Thread):
    '''
       Integration layer is used to convert an action detected by the AI model, into a message that can
       be sent to the frontend via the socket connection.
    '''
    def __init__(self, event_bus, sock):
        super().__init__()
        self.socketio = sock
        self.event_bus = event_bus
        self.log = {}
        self.activity = []

    def maybe_initialize_user(self, user: str):
        print("maybe_initialize_user")
        if user not in log:
            log[user] = {
                'id': len(activity),
                'name': user,
                'logs': [],
            }

    def send_notifications_to_client(self, username, action):
       message = {
           'user': username,
           'action': action
       }
       self.socketio.emit('notifications', message)

    def detected_user_action(self, user: str, image: str, cleaned: bool):
        # Send notification
        print("Sending notification [user_added_plates] to frontend")
        curr_time = datetime.now().strftime('%I:%M:%S %p')

        message = " cleaned the dishes!" if cleaned else "added plates to the sink"

        send_notifications_to_client(user, message)

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
        self.socketio.emit(activity[::-1])


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

        list_log = []
        for key in log.keys():
            list_log.append(log[key])

        # must reverse activity to show the latest event first
        self.socketio.emit('log', list_log[::-1])

    def run(self):
        print("Integration Layer started")
        while True:
            event = self.event_bus.subscribe()
            if event is None:
                break  # Stop the thread
            print(f"Integration layer received event: {event}")
            if event['type'] == 'user_action':
                self.detected_user_action(event)
            elif event['type'] == 'suspect_frame':
                self.send_notifications_to_client(event['user'], event['message'])
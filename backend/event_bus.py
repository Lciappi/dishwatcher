import threading
import queue

class EventBus:
    '''
        The EventBus is used to communicate between layers in a thread-safe way
        without causing a circular dependency.
    '''
    def __init__(self):
        self.events = queue.Queue()

    def publish(self, event):
        print(f"EventBus: Publishing event {event}")
        self.events.put(event)

    def subscribe(self):
        print("EventBus: Subscribing to events")
        return self.events.get()


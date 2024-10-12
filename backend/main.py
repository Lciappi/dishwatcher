from flask import Flask
from flask_socketio import SocketIO
from event_bus import EventBus
from integration_layer import IntegrationLayer
from logic_layer import LogicLayer
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS configuration [allow frontend]
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

event_bus = EventBus()

integration_layer = IntegrationLayer(event_bus, socketio)
integration_layer.start()

logic_layer = LogicLayer(event_bus)
logic_layer.start()

@app.route('/')
def index():
    return "Server is running!"

if __name__ == "__main__":
    print("Starting Server")
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
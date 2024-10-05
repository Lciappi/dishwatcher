import pytest
from flask import Flask
from flask_socketio import SocketIO, SocketIOTestClient
from main import app, socketio, send_message_to_client

@pytest.fixture
def client():
    # Create a test client for the Flask application
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def socketio_client(client):
    # Create a test client for Socket.IO
    return SocketIOTestClient(app, socketio)

def test_hello(socketio_client):
    with app.app_context():
        # socketio_client.emit('hello', "Hello from the server!")
        send_message_to_client()
        received = socketio_client.get_received()

        assert len(received) == 1
        assert received[0]['name'] == 'hello'
        assert received[0]['args'] == ['Hello from the server!']
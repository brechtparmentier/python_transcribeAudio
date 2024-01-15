# shared.py
from flask_socketio import SocketIO

socketio = SocketIO()

def get_socketio():
    return socketio

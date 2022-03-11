import os
# import requests
import logging
# from time import sleep
# import sys

from flask import Flask, jsonify, render_template, request, session
from flask_socketio import SocketIO, emit,join_room, leave_room


# NOTA: https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice


app = Flask(__name__, static_url_path='')
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

socketio = SocketIO(app,cors_allowed_origins="*",ping_timeout=10,ping_interval=25)
    # :param ping_timeout: The time in seconds that the client waits for the
    #                      server to respond before disconnecting. The default is
    #                      60 seconds.
    # :param ping_interval: The interval in seconds at which the client pings
    #                       the server. The default is 25 seconds.
logging.basicConfig(level=logging.DEBUG)


# INITIAL CONFIGURATION
switches = {"onoff": False, "recording": False,"hide_peer":True,"peer_hostname":""}
HOST = "0.0.0.0"
WEB_PORT = 5000

print("hello")

# @app.route("/")
# def index():
#     # global camerautility
#     # camerautility = CameraUtility()
#     output = render_template(
#         "index.html", switches=switches, async_mode=socketio.async_mode)
#     return output


import random

webclients = []
camera_clients = []


# WEBCLIENTS----------------------------
@socketio.event
def connect():
    print("connected. sid:", request.sid)
    webclients.append(request.sid)
    emit('CONNECTED_CAMERAS', {'cameras': camera_clients}, broadcast=True)
    
@socketio.on('disconnect')
def disconnect():
    print('Web Client disconnected: ', request.sid)
    webclients.remove(request.sid)

@socketio.on('CHANGE_SETTINGS')
def change_settings(data):
    '''
    change settings for cameras
    Example data::
        data = {
            "camera_id": "HzXVJcOJdvd72RAIAAAD",
            "settings": {iso: 100}
            }
    Example data::
        data = {
            "camera_id": "ALL",
            "settings": {iso: 100}
            }
    '''
    if not 'settings' in data or not 'camera_id' in data:
        print("ERROR: CHANGE_SETTINGS: no settings or camera_id in data",data)
        return
    if data['camera_id'] == "ALL":
        emit('CHANGE_SETTINGS', data['settings'], namespace='/camera',broadcast=True)
        print("CHANGE_SETTINGS/camera - TOALL", data['settings'])
    else:
        emit('CHANGE_SETTINGS', data['settings'], namespace='/camera',broadcast=True,room=data['camera_id'])
        print(f"CHANGE_SETTINGS/camera - TO:{data['camera_id']}", data['settings'])


# CAMERAS --------------------------

@socketio.on('connect', namespace='/camera')
def camera_connect():
    print("camera connected. sid:", request.sid)
    camera_clients.append(request.sid)
    emit('CONNECTED_CAMERAS', {'cameras': camera_clients}, broadcast=True,namespace='/')
    join_room(request.sid)

@socketio.on('disconnect', namespace='/camera')
def camera_disconnect():
    print('Camera disconnected: ', request.sid)
    camera_clients.remove(request.sid)
    print(camera_clients)
    emit('CONNECTED_CAMERAS', {'cameras': camera_clients}, broadcast=True,namespace='/')
    leave_room(request.sid)


# @socketio.on('joined', namespace='/camera')
# def joined(message):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     join_room(room)
#     # emit to the first client that joined the room
#     emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=clients[0])


if __name__ == "__main__":
    # socketio.run(app, port=5000, host='0.0.0.0', debug=True, use_reloader=False,pingInterval=1000, pingTimeout=2000)
    socketio.run(app, port=5000, host='0.0.0.0', debug=True, use_reloader=False)


# if __name__ == "__main__":

#     # # starting the web server
#     webserver = WebServerThread(app, HOST, WEB_PORT)
#     webserver.start()
#     logging.info("Started Flask web server")

#     # and run it indefinitely
#     try:
#         while True:
#             sleep(0.5)
#     except KeyboardInterrupt:
#         print("Keyboard interrupt")
#     # until some keyboard event is detected

#     # trigger shutdown procedure
#     webserver.shutdown()

#     # and finalize shutting them down
#     webserver.join()
#     logging.info("Stopped Flask web server")

#     sys.exit(0)

import os
# import requests
import logging
# from time import sleep
# import sys

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

# from threading import Condition, Event, Thread


# from src.picamera_video import CameraUtility
# camerautility = CameraUtility()
initial_message = "Status: Camera Ready"
try:
    from src.picamera_video import CameraServer
    camerautility = CameraServer()
    camerautility.init_server()
except:
    class CameraServer_DUMMY(object):
        def __init__(self, *args, **kwargs):
            pass
        def start_streaming(self):
            pass
        def stop_streaming(self):
            pass
        def start_recording(self):
            pass
        def stop_recording(self):
            pass
        def get_peer_name(self):
            return None
        def close(self):
            pass
    camerautility = CameraServer_DUMMY()
    initial_message = 'CANNOT LOAD CAMERA'

# NOTA: https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice


app = Flask(__name__, static_url_path='')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


socketio = SocketIO(app,cors_allowed_origins="*")
logging.basicConfig(level=logging.DEBUG)


# INITIAL CONFIGURATION
switches = {"onoff": False, "recording": False,"hide_peer":True,"peer_hostname":""}
HOST = "0.0.0.0"
WEB_PORT = 5000

print("hello")

@app.route("/")
def index():
    # global camerautility
    # camerautility = CameraUtility()
    output = render_template(
        "index.html", switches=switches, async_mode=socketio.async_mode)
    return output
#{% comment %} <img onerror="this.src='image.jpg'" src="image.jpg" width="400" height="300"> {% endcomment %}
    # <script language="JavaScript">
    #         document.write('<img id="video_source" src="' + window.location.protocol + '//' + window.location.hostname + ':8000' + '/stream.mjpg' + '" width="400" height="300" />' );
    # </script>


@socketio.on("connect")
def initial_setup():
    emit("initial message",initial_message,broadcast=True)
    emit("update switches", switches, broadcast=True)
    emit("resolution change", {'resolution':'320x240'}, broadcast=True)


@socketio.on("switch change")
def switch_change(data):
    '''
    turn camera on or off
    '''
    key = list(data.keys())[0]
    switches[key] = data[key]
    if key == 'onoff':
        if switches[key] is True:
            camerautility.start_streaming()
            peer_hostname = camerautility.get_peer_name()
            if peer_hostname is not None:
                switches["hide_peer"]=False
                switches["peer_hostname"]=peer_hostname
        else:
            camerautility.stop_streaming()
    elif key == 'recording':
        if switches[key] is True:
            camerautility.start_recording()
        else:
            camerautility.stop_recording()
    print(switches)
    emit("update switches", switches, broadcast=True)

@socketio.on("resolution change")
def resolution_change(data):
    resolution = data['resolution']
    if resolution == '1920x1080':
        camerautility.change_stream_resolution('1920x1080')
    elif resolution == '320x240':
        camerautility.change_stream_resolution('320x240')
    else:
        print('resolution not supported')


try:
    socketio.run(app, port=5000, host='0.0.0.0', debug=True, use_reloader=False)
finally:
    camerautility.close()


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

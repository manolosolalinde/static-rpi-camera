import socketio
from src.camera_initializer import initialize_camera

# sio = socketio.Client(reconnection=False,handle_sigint=True)

class MySocketIOClient(socketio.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __del__(self):
        print('Client is closed')

sio = MySocketIOClient(reconnection=False,handle_sigint=True)


@sio.event
def connect():
    print('connection established')

@sio.on('connect',namespace='/camera')
def camera_connect():
    print('camera connected')




# initialize camera
cameracontroller = initialize_camera()


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on('update live parameters')
def switch_change(data):
    print(data)

@sio.on('CHANGE_SETTINGS',namespace='/camera')
def change_settings(data):
    print('CHANGE_SETTINGS/camera')
    print(data)

def main():
    while True:
        try:
            sio.connect('http://localhost:5000',wait_timeout=10,namespaces=['/camera'])
            # import code
            # code.interact(local=dict(globals(), **locals()))
            sio.wait()
        except socketio.exceptions.ConnectionError as e:
            print('retrying connection... to http://localhost:5000')
            sio.sleep(1)
        finally:
            sio.disconnect()
            

main()

# sio.connect('http://localhost:5000',wait_timeout=10,)
# sio.wait()


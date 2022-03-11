
def initialize_camera():
    try:
        from src.camera_controller import CameraController
        cameracontroller = CameraController()
        initial_message = "Status: Camera Ready"
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
        cameracontroller = CameraServer_DUMMY()
        initial_message = 'Dummy Camera loaded'
    print(initial_message)
    return cameracontroller

if __name__ == "__main__":
    cameracontroller = initialize_camera()
    import code
    code.interact(local=dict(globals(), **locals()))

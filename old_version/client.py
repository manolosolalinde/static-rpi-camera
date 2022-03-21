from src.picamera_video import CameraClient
import sys

if __name__ == "__main__":
    camclient = CameraClient()
    camclient.init_client()
    camclient.close()
    sys.exit(0)
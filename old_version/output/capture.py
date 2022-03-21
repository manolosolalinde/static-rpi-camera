from time import sleep
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = '1080p' #(1920, 1080)
camera.vflip = True
camera.hflip = True
camera.start_preview()
# Camera warm-up time
sleep(2)
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = 'snap-' + timestr + '-%03d.jpg'
camera.capture(filename)
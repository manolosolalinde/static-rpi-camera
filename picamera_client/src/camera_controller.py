
# imports needed for stream server
import io
import logging
# import signal
import socketserver
import subprocess
import sys
# import time
from http import server
from threading import Condition, Event, Thread
from time import sleep

import picamera
import signal

import os
import shlex

import time



logging.basicConfig(level=logging.DEBUG)


class CameraController():
    def __init__(self, *args, **kwargs):
        '''
        Nota resoluciones: https://picamera.readthedocs.io/en/release-1.12/fov.html
        '''
        self.camera = picamera.PiCamera(resolution='1296x972', framerate=25)#1920x1080
        # self.camera = picamera.PiCamera(resolution='1920x1080', framerate=25)#1920x1080
        self.STREAM_PORT = 8000
        self.HOST = ''
        global output_mustbelocal
        output_mustbelocal = self.StreamingOutput()
        print("camera initialized")
        self._audiodev = self.getaudiodevice()
        self.stream_resolution = '320x240'
        self.stream = None

    # to be overriden
    def init(self):
        pass

    def close(self):
        self.camera.close()
        print("camera closed")

    def getaudiodevice(self):
        devices = os.popen("arecord -l")
        device_string = devices.read()
        device_string = device_string.split("\n")
        for line in device_string:
                if(line.find("card") != -1):
                    audiodev = "hw:" + line[line.find("card")+5] + "," +\
                    line[line.find("device")+7]
                    return audiodev
        return None
    
    def change_live_parameters(self,parameters):
        '''
        check https://picamera.readthedocs.io/en/release-1.12/api_camera.html
        '''
        default_parameters = {
            'brigthness':50,
            'brigthness_limits':[0,100],
            'contrast':0,
            'contrast_limits':[-100,100],
            'saturation':0,
            'saturation_limits':[-100,100],
            'sharpness':0,
            'sharpness_limits':[-100,100],
            'shutter_speed':0,
            'shutter_speed_limits':[0,60000],
            'exposure_compensation':0,
            'exposure_compensation_limits':[-25,25],
            'iso':0,
            'iso_limits':[0,1600],
            '':0,
            '_limits':[-100,100],
            '':0,
            '_limits':[-100,100],
            'awb_mode':'auto',
            'awb_mode_options':['off','auto','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon'],
            'exposure_mode':'auto',
            'exposure_mode_options':['off','auto','night','nightpreview','backlight','spotlight','sports','snow','beach','verylong','fixedfps','antishake','fireworks']
        }


    def change_stream_resolution(self,resolution='320x240'):
        if resolution == self.stream_resolution:
            return
        if self.stream is None:
            self.stream_resolution = resolution
            return
        else:
            self.stream_resolution = resolution
            self.stop_streaming()
            self.start_streaming(resolution)

    def start_streaming(self,resolution='320x240'):
        '''
        compare with: raspivid -o myvid.h264 -w 1920 -h 1080
        '''
        # firing up the video camera (pi camera)
        # self.camera.vflip = True
        # self.camera.hflip = True
        # self.camera.zoom = (0.35,0.35,0.3,0.3)
        self.stream_resolution = resolution
        if resolution == '320x240':
            self.camera.start_recording(output_mustbelocal, resize=(
                320, 240), format='mjpeg', splitter_port=1) #1920x1080 #320x240
        elif resolution == '1920x1080':
            self.camera.start_recording(output_mustbelocal, resize=(
                1920, 1080), format='mjpeg', splitter_port=1) #1920x1080 #320x240
        # self.camera.start_recording(output_mustbelocal, format='mjpeg', splitter_port=2)
        logging.info("Started streaming with picamera")

        self.stream = self.StreamingServer(
            (self.HOST, self.STREAM_PORT), self.StreamingHandler)

        # # starting the video streaming server
        self.streamserver = Thread(target=self.stream.serve_forever)
        self.streamserver.start()
        logging.info("Started stream server for picamera")

    def start_recording(self):

        audiodev = self.getaudiodevice()
        hostname = socketserver.socket.gethostname()
        timestr = time.strftime("%Y_%m_%d_%H%M%S") + "rp" + hostname[-1:]
        audiofilename = 'out-' + timestr +'.aac'
        videofilename = 'out-' + timestr +'.h264'
        filename = 'out-' + timestr + '-%03d.mp4'
        os.system("echo "+str(time.time())+ "> ./output/out-"+timestr+"-start.txt")

        if 1==1:
            #record audio and video separated:
            if audiodev == "hw:1,0":
                print("Recording audio...")
                stream_cmd = 'ffmpeg -loglevel info -use_wallclock_as_timestamps 1 -f alsa -ac 1 -r 25 -y -i hw:1,0' + \
                    ' -acodec aac -ac 1 -ar 8000 -ab 32k -strict experimental -r 25 ./output/' + audiofilename
                stream_cmd = shlex.split(stream_cmd)
                self.stream_pipe = subprocess.Popen(stream_cmd, shell=False,stdin=subprocess.PIPE, preexec_fn = os.setpgrp)
            self.camera.start_recording('./output/' + videofilename, format='h264', bitrate=2000000, splitter_port=2)
            
    
        else:
            #record mixed audio and video and segment
            stream_cmd = 'ffmpeg -thread_queue_size 512 -loglevel info -use_wallclock_as_timestamps 1 -f h264 -y -i -' + \
                ' -f alsa -ac 1 -r 25 -i hw:1,0 -ss 1.0 ' + \
                ' -vcodec copy -acodec aac -ac 1 -ar 8000 -ab 32k ' + \
                ' -map 0:0 -map 1:0 -strict experimental -r 25 ' + \
                ' -segment_time 00:20:00 -f segment -reset_timestamps 1 -segment_list ./output/Test.ffcat ' + './output/' + filename
            #para agregar tiempo a cada frame
            #nota: ffmpeg -i input -vf "drawtext=fontfile=/Windows/Fonts/Arial.ttf: text='%{localtime}': x=(w-tw)/2: y=h-(2*lh): 
            # fontcolor=white: box=1: boxcolor=0x00000000@1: fontsize=30" -r 25 -t 5 image%03d.png
            #linea 3 final -filter:a "volume=+15dB"
            # 25.375 from https://raspberrypi.stackexchange.com/questions/25962/sync-audio-video-from-pi-camera-usb-microphone
            #-fflags nobuffer
            # -r 25
            # stream_cmd = 'ffmpeg -loglevel -8 -r 25 -y -i - -itsoffset 5.5 -fflags' + \
            #     ' nobuffer -use_wallclock_as_timestamps 1 -f alsa -ac 1 -i hw:1,0' + \
            #     ' -vcodec libx265 -acodec aac -ac 1 -ar 8000 -ab 32k -filter:a "volume=+15dB" ' + \
            #     ' -map 0:0 -map 1:0 -strict experimental ' + \
            #     ' -segment_time 00:20:00 -f segment -reset_timestamps 1 -segment_list ./output/Test.ffcat ' + './output/' + filename
            stream_cmd = shlex.split(stream_cmd)
            self.stream_pipe = subprocess.Popen(stream_cmd, shell=False, stdin=subprocess.PIPE,preexec_fn = os.setpgrp)
            # NOTA: Recomendacion de exec +  
            # en https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
            # sleep()
            self.camera.start_recording(
                self.stream_pipe.stdin, format='h264', bitrate=2000000, splitter_port=2)
        logging.info("Started recording to stream with picamera")

    def stop_recording(self):

        # finalize streaming to custom output
        self.camera.stop_recording(splitter_port=2)
        logging.debug("camera stop_recording spliter_port=2")

        # stop ffmpeg
        try:
            self.stream_pipe.send_signal(signal.SIGINT)
            
            #wait to finish
            if self.stream_pipe.poll() != 0:
                try:
                    self.stream_pipe.wait(1)
                except:
                    pass
        except:
            pass

        logging.debug("ffmpeg process finished")

        #necesario para cerrar
        self.stream_pipe.stdin.close()

        logging.info("Camera Stopped recording")

    def stop_streaming(self):
        self.camera.stop_recording(splitter_port=1)
        logging.info("Camera Stopped streaming")

        # trigger shutdown procedure
        self.stream.shutdown()
        self.stream.server_close()

        # and finalize shutting them down
        self.streamserver.join()
        self.stream = None
        # self.streamserver._delete()

        # import code
        # code.interact(local=dict(globals(), **locals()))

        logging.info("Stopped stream server")

    def __del__(self):
        print("CameraUtility Instance deleted")
        # self.camera.close()

    def get_peer_name(self):
        return None

    class StreamingOutput(object):
        '''
        Class to which the video output is written to.
        The buffer of this class is then read by StreamingHandler continuously.
        '''

        def __init__(self):
            self.frame = None
            self.buffer = io.BytesIO()
            self.condition = Condition()

        def write(self, buf):
            if buf.startswith(b'\xff\xd8'):
                # New frame, copy the existing buffer's content and notify all
                # clients it's available
                self.buffer.truncate()
                with self.condition:
                    self.frame = self.buffer.getvalue()
                    self.condition.notify_all()
                self.buffer.seek(0)
            return self.buffer.write(buf)

    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True
        # def __init__(self,*args,**kwargs) -> None:
        #     super().__init__()


    class StreamingHandler(server.BaseHTTPRequestHandler):
        '''
        Implementing GET request for the video stream.
        '''

        def do_GET(self):

            PAGE = """\
            <html>
            <head>
            <title>picamera MJPEG streaming demo</title>
            </head>
            <body>
            <h1>PiCamera MJPEG Streaming Demo</h1>
            <img src="stream.mjpg" width="640" height="480" />
            </body>
            </html>
            """ #640x480
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header(
                    'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with output_mustbelocal.condition:
                            output_mustbelocal.condition.wait()
                            frame = output_mustbelocal.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            else:
                self.send_error(404)
                self.end_headers()

if __name__ == "__main__":

    camerautility = CameraController()
    camerautility.start_streaming()
    # camerautility.start_recording()
    print(output_mustbelocal)
    try:
        while True:
            sleep(0.5)
            # print("Sleep")
    except KeyboardInterrupt:
        print("Keyboard interrupt")

    # camerautility.stop_recording()
    camerautility.stop_streaming()
    camerautility.close()
    sys.exit(0)

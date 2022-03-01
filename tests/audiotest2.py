import os

def getaudiodevices2():
    devices = os.popen("arecord -l")
    device_string = devices.read()
    device_string = device_string.split("\n")
    for line in device_string:
            if(line.find("card") != -1):
                print("hw:" + line[line.find("card")+5] + "," +\
 line[line.find("device")+7])

import pyaudio

def getaudiodevices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i).get('name'))

getaudiodevices2()



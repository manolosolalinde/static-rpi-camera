import subprocess
import signal
from time import sleep
import shlex
import os
# file_object = open("text.txt","w")
command = shlex.split("python aux2.py > test.txt")
# os.setpgrp from 
# https://stackoverflow.com/questions/5045771/python-how-to-prevent-subprocesses-from-receiving-ctrl-c-control-c-sigint

def pre_exec():
    # To ignore CTRL+C signal in the new process
    os.setpgrp()

test = subprocess.Popen(command,shell=False,preexec_fn = os.setpgrp,stdin=subprocess.PIPE)
print("process initiated")

try:
    while True:
        sleep(0.5)
        print("Running..")
except KeyboardInterrupt:
    print("Keyboard interrupt....")

print("sending interrupt signal")
test.send_signal(signal.SIGINT)
if test.poll() is None:
    print("process is not yet terminated")
status = test.wait()
if status == 0:
    print("process is terminated")



# import code
# code.interact(local=dict(globals(), **locals()))

#!/bin/bash
# Installation file to make the Camera Robot start on boot.
# This will add the camerarobot start on boot to SystemD on Stretch
sudo cp replaybox.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/replaybox.service
sudo systemctl daemon-reload
sudo systemctl enable replaybox.service

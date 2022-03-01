#!/bin/bash
# Installation file to make Replaybox Client service (replaybox002)
# This will add the replaybox_service start on boot to SystemD on Stretch
sudo cp replaybox_client.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/replaybox_client.service
sudo systemctl daemon-reload
sudo systemctl enable replaybox_client.service

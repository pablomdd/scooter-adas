#!/bin/bash

echo "***********Looter, the scooter. A scooter ADAS***********"
echo "Running startup script..."
cd ~/Documents/github/scooter-adas/tf_detector
# Replace with user password or set environment variable to reference
echo "$USER_PASSWORD" | sudo -S python3 adas.py -dev=False
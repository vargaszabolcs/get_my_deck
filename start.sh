#!/bin/bash

# Try to start the Mullvad daemon using systemctl
sudo systemctl start mullvad-daemon || sudo /usr/bin/mullvad-daemon -v
sleep 2

# Login with account number
mullvad account login ${MULLVAD_ACCOUNT}
sleep 2

# Set location and connect
mullvad relay set location ro
mullvad connect
sleep 5

# Start the application
gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 2 --worker-class gthread --timeout 0 get_my_deck:app

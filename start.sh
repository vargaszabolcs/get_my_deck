#!/bin/bash
mullvad account login ${MULLVAD_ACCOUNT}
mullvad relay set location ro
mullvad connect
sleep 5
gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 2 --worker-class gthread --timeout 0 get_my_deck:app

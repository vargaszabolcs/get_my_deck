#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1024x768x16 &

# Start the application
gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 2 --worker-class gthread --timeout 0 get_my_deck:app

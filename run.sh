#!/bin/bash

set -e

# Change directory to the script's directory
cd "$( dirname "${BASH_SOURCE[0]}" )"

# Build frontend
if ! [ -d dist ]; then
    npm install
    npm run build
fi

# Set up environment for backend
if ! [ -d .venv ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install uwsgi
else
    source .venv/bin/activate
fi

# Serve the application (customize this per-deployment)
uwsgi \
    --http-socket 0.0.0.0:8387 \
    --processes 1 --threads 8 \
    --disable-logging --log-4xx --log-5xx \
    --wsgi-file simple_wol.py --callable app

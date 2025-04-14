#!/bin/bash

args="$@"

if [[ "$args" == *"dev"* ]]; then
    echo "Starting development server..."
    export PYTHONPATH=src
    fastapi dev main.py --reload
elif [[ "$args" == *"prod"* ]]; then
    echo "Starting production Uvicorn server..."
    export PYTHONPATH=src
    python uvicorn.conf.py
else
    echo "Starting development server as default"
    export PYTHONPATH=src
    fastapi dev main.py --reload
fi
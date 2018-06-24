#!/bin/bash
if ! screen -list | grep -q "feature_requests"; then
    source venv/bin/activate
    export FLASK_APP=app/main.py
    export FLASK_DEBUG=1
    flask run --host 0.0.0.0
else
    echo -e "\033[1;33mFeatureRequests\033[1;31m app is running already in normal mode.\033[0m";
fi
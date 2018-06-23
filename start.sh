#!/bin/bash
if ! screen -list | grep -q "feature_requests"; then
    screen -dmS feature_requests bash -c "
        source venv/bin/activate
        export FLASK_APP=app/main.py
        flask run";
    echo -e "\033[1;32mStarted \033[1;33mFeatureRequests\033[1;32m app.\033[0m";
else
    echo -e "\033[1;33mFeatureRequests\033[1;31m app is running already.\033[0m";
fi
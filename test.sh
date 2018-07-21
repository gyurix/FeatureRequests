#!/bin/bash
if ! screen -list | grep -q "feature_requests"; then
    screen -dmS feature_requests bash -c "
        source venv/bin/activate
        pytest -v tests.py
        sleep 3"
    echo -e "\033[1;32mLaunched \033[1;33mFeatureRequests\033[1;32m testing.\033[0m";
    sleep 1
    screen -x feature_requests
else
    echo -e "\033[1;33mFeatureRequests\033[1;31m app is running already.\033[0m";
fi
#!/bin/bash
if screen -list | grep -q "feature_requests"; then
    screen -X -S feature_requests quit
    echo -e "\033[1;32mStopped \033[1;33mFeatureRequests\033[1;32m app.\033[0m"
else
    echo -e "\033[1;33mFeatureRequests\033[1;31m app is not running.\033[0m"
fi
#!/bin/bash
if screen -list | grep -q "feature_requests"; then
    echo -e "\033[1;33mFeatureRequests\033[1;32m app is running\033[0m"
else
    echo -e "\033[1;33mFeatureRequests\033[1;31m app is not running\033[0m"
fi

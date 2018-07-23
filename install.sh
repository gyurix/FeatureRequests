#!/bin/bash
echo -e '\033[1;36mInstalling \033[1;33mPython\033[1;36m...\033[0m'
apt-get update
apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install -y python3.6
echo -e '\033[1;36mInstalling \033[1;33mFlask\033[1;36m...\033[0m'
rm -Rf venv
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip3.6 install -r requirements.txt
chmod 770 start.sh stop.sh status.sh debug.sh test.sh
#!/bin/bash
echo -e '\033[1;36mInstalling \033[1;33mPython\033[1;36m...\033[0m'
apt-get -y install python3-dev python3-pip
echo -e '\033[1;36mInstalling \033[1;33mFlask\033[1;36m...\033[0m'
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
chmod 770 start.sh stop.sh status.sh debug.sh test.sh
#!/bin/bash
set -e
export DISPLAY=:1.0
export MIST_URL=${MIST_URL:-http://172.17.0.1}
export VNC=${VNC:-}
args=$@

if [ -z "$VNC" ]
then
    echo Headless mode
else
    XVFB_WHD=${XVFB_WHD:-1280x1024x16}
    Xvfb :1 -ac -screen 0 $XVFB_WHD &
    x11vnc -nopw -display :1.0 -listen 0.0.0.0 -rfbport 5900 &
    echo VNC server started
fi

mkdir /data
cd /data
python -m SimpleHTTPServer 8222 2&>1 > /dev/null &

sleep 2

cd /mist.tests
clear

source ./vault_login.sh

./run_tests.sh $args
echo "./run_tests.sh $args" > ~/.bash_history
/bin/bash

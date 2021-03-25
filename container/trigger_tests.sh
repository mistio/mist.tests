#!/bin/bash
set -e
export MIST_URL=${MIST_URL:-http://172.17.0.1}
export VNC=${VNC:-}
args=$@

if [ -z "$VNC" ]
then
    echo Headless mode
else
    source /mist.tests/run_vnc_server.sh
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

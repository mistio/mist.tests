#!/bin/bash
set -e
export DISPLAY=:1.0
export MIST_URL=${MIST_URL:-http://172.17.0.1}

mkdir /data
cd /data
python -m SimpleHTTPServer 8222 2&>1 > /dev/null &

cd /mist.core/mist.io/tests

/bin/bash

#!/bin/bash

set -e

export DISPLAY=:1.0
export MIST_URL=${MIST_URL:-http://172.17.0.1}

x11vnc -nopw -display :1.0 -listen 0.0.0.0 -rfbport 5900 &

# if below commented out, ipdb not working
cd /mist.core/mist.io/tests

sleep .5

/bin/bash

#!/usr/bin/env bash
export DISPLAY=:1.0
XVFB_WHD=${XVFB_WHD:-1280x1024x16}
Xvfb :1 -ac -screen 0 $XVFB_WHD &
x11vnc -nopw -display :1.0 -listen 0.0.0.0 -rfbport 5900 &
echo VNC server started

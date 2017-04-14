#!/bin/sh

x11vnc -display :1.0 -listen 0.0.0.0 -rfbport 5900 &

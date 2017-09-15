#!/bin/bash

set -e

export DISPLAY=:1.0
export MIST_URL=${MIST_URL:-http://172.17.0.1}

cd /mist.core/mist.io/tests

sleep .5

/bin/bash

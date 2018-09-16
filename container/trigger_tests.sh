#!/bin/bash
set -e
export DISPLAY=:1.0
export MIST_URL=${MIST_URL:-http://172.17.0.1}
export VNC=${VNC:-}
args=$@

vault_login() {
    if [ -z "$VAULT_CLIENT_TOKEN" ]
    then
        export vault_server=${VAULT_ADDR:-https://vault.ops.mist.io:8200}
        echo Vault username:
        read username
        echo Vault password:
        read -s password
        export PYTHONIOENCODING=utf8

        VAULT_CLIENT_TOKEN=$(
          curl -sSk $vault_server/v1/auth/userpass/login/$username -d '{ "password": "'${password}'" }' |
          python -c "
import sys, json;
res = json.load(sys.stdin)
if res.get('auth'):
    print(res['auth']['client_token'])"
        )

        if [[ -z "${VAULT_CLIENT_TOKEN// }" ]]
        then
            echo 'Wrong credentials given...'
            vault_login
        else
            export VAULT_CLIENT_TOKEN
            echo 'Successfully logged in.'
        fi
    fi
}

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
vault_login

./run_tests.sh $args
echo "./run_tests.sh $args" > ~/.bash_history
/bin/bash

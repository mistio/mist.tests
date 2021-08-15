#!/bin/bash
set -e
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
        url=${vault_server}/v1/auth/userpass/login/${username}
        VAULT_CLIENT_TOKEN=$(
          curl -sSk $url -d "{ \"password\": \"${password}\" }" |
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

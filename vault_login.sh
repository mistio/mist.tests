#!/usr/bin/env bash

vault_login() {
    if [ -z "$VAULT_CLIENT_TOKEN" ]
    then
        export vault_server=${VAULT_ADDR:-https://vault.ops.mist.io:8200}
        echo Vault username:
        read username
        echo Vault password:
        read -s password
        export PYTHONIOENCODING=utf8
        password_json='{"password":"'"$password"'"}'
        VAULT_CLIENT_TOKEN=$(
          curl -k "$vault_server"/v1/auth/userpass/login/"$username" -d "$password_json" |
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
            echo 'Successfully logged in. About to start running tests...'
        fi
    fi
}

if [ "${1}" != "--source-only" ]; then
    vault_login
fi

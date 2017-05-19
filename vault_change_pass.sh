#!/bin/bash

set_password() {
    echo Please type your new Vault password:
    read -s new_password
    echo Please type your new Vault password again:
    read -s new_password_repeat
    if [ "$new_password" == "$new_password_repeat" ]
    then
        curl -X POST -H "X-Vault-Token:$vault_client_token" https://vault.ops.mist.io:8200/v1/auth/userpass/users/$username/password  -d '{ "password": "'$new_password'" }'
        echo 'Password reset was successful!'
    else
        echo Passwords do not match...
        set_password
    fi
}

echo Please type your Vault username:
read username
echo Please type your current Vault password:
read -s password
vault_client_token=$(curl https://vault.ops.mist.io:8200/v1/auth/userpass/login/$username -d '{ "password": "'${password}'" }' |
     python -c "import sys, json; print(json.load(sys.stdin)['auth']['client_token'])")


if [ -z "$vault_client_token" ]
then
    echo 'Wrong credentials given.Exiting...'
    exit
else
    set_password
fi

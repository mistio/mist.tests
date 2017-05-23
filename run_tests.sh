#!/bin/bash

help_message() {
    echo
    echo "Usage: ./run_tests.sh [option] {argument}"
    echo
    echo "Options:"
    echo
    echo "[no option]   First API tests and then GUI tests will be invoked"
    echo "-h            Display this message"
    echo "-api          Run api tests suite. If no argument provided, the entire API tests suite will be invoked"
    echo "-gui          Run gui tests suite. If no argument provided, the entire GUI tests suite will be invoked"
    echo
    echo "Argument for API tests can be one of the following:"
    echo
    echo "clouds, machines, tunnels, keys, scripts, api_token, tunnels, schedules, orchestration"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, machines, images, keys, scripts, users, rbac, schedules, orchestration"
    echo
    exit
}

run_gui_tests_suite() {
    behave_tags=""
    for tag in "${behave_tags[@]}"
    do
      behave_tags+="${tag}"
    done
    behave -k --tags=$behave_tags misttests/gui/core/pr/features
}

run_api_tests_suite() {
    pytest_args=""
    for path in "${pytest_paths[@]}"
    do
      pytest_args="${pytest_args} ${path}"
    done
    pytest -s $pytest_args
}

vault_login() {
    export vault_server=${VAULT_ADDR:-https://vault.ops.mist.io:8200}
    echo Vault username:
    read username
    echo Vault password:
    read -s password
    export PYTHONIOENCODING=utf8
    vault_client_token=$(curl $vault_server/v1/auth/userpass/login/$username -d '{ "password": "'${password}'" }' |
     python -c "import sys, json; print(json.load(sys.stdin)['auth']['client_token'])")

    if [ -z "$vault_client_token" ]
    then
        echo 'Wrong credentials given...'
        vault_login
    else
        export vault_client_token
        echo 'Successfully logged in. About to start running tests...'
    fi
}

    declare -A pytest_paths

    pytest_paths["clouds"]='misttests/api/io/clouds.py'
    pytest_paths["images"]='misttests/api/io/images.py'
    pytest_paths["machines"]='misttests/api/io/machines.py'
    pytest_paths["keys"]='misttests/api/io/keys.py'
    pytest_paths["dns"]='misttests/api/io/dns.py'
    pytest_paths["scripts"]='misttests/api/io/scripts.py'
    pytest_paths["tunnels"]='misttests/api/io/tunnels.py'
    pytest_paths["api_token"]='misttests/api/io/api_token.py'
    pytest_paths["schedules"]='misttests/api/io/schedules.py'
    pytest_paths["orchestration"]='misttests/api/core/orchestration.py'

    declare -A behave_tags

    behave_tags["clouds"]='clouds-add-a','clouds-add-b','clouds-actions,'
    behave_tags["images"]='images-networks,'
    behave_tags["keys"]='keys,'
    behave_tags["scripts"]='scripts,'
    behave_tags["machines"]='machines,'
    behave_tags["users"]='user-actions,'
    behave_tags["rbac"]='rbac-rules','rbac-teams','rbac-rules-v2,'
    behave_tags["schedules"]='schedulers','schedulers_v2,'
    behave_tags["orchestration"]='orchestration,'



    if [ "$#" -eq 0 ]
    then
        vault_login
        run_api_tests_suite
        run_gui_tests_suite
        exit
    fi

    if [ $1 == '-h' ] || [ "$#" -gt 2 ]
    then
        help_message
        exit
    fi

    if [ "$#" -lt 2 ]
    then
        if [ $1 == '-api' ]
        then
            vault_login
            run_api_tests_suite
            exit
        elif [ $1 == '-gui' ]
        then
            vault_login
            run_gui_tests_suite
        else
            help_message
        fi
    else
       if [ $1 == '-api' ] && [[ " ${!pytest_paths[@]} " == *" $2 "* ]]; then
            vault_login
            pytest -s ${pytest_paths["$2"]}
       elif [ $1 == '-gui' ] && [[ " ${!behave_tags[@]} " == *" $2 "* ]]; then
            vault_login
            behave -k --stop --tags=${behave_tags["$2"]} misttests/gui/core/pr/features
       else
            help_message
       fi
    fi


# fix safe_get_var

# fix and test run_tests.sh

# update README.md

# use_Vault_for_more_vars

# move core_tests (+rm gui/core...)

#!/bin/bash

help_message() {
    echo
    echo "Usage: ./run_tests.sh [-t] [option] {argument}"
    echo
    echo "-t"           If given, then all variables will be read from test_settings.py,
    echo                otherwise, Vault credentials will be asked.
    echo
    echo "Options:"
    echo
    echo "[no option]   First API tests and then GUI tests will be invoked"
    echo "-h            Display this message"
    echo "-api          Run api tests suite. If no argument provided, the entire API tests suite will be invoked"
    echo "-gui          Run gui tests suite. If no argument provided, the entire GUI tests suite will be invoked"
    echo "-provision    Run libcloud provision test."
    echo
    echo "Argument for API tests can be one of the following:"
    echo
    echo "clouds, machines, tunnels, keys, dns, scripts, api_token, tunnels, schedules, orchestration, libcloud, networks, rbac"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, clouds-actions, machines, images, keys, scripts, users, rbac, schedules, orchestration, monitoring, rbac-rules, insights"
    echo
    exit
}

run_gui_tests_suite() {
    # behave_tags=""
    # for tag in "${behave_tags[@]}"
    # do
    #   behave_tags+="${tag}"
    # done

    behave -k --no-capture --no-capture-stderr --tags=clouds-actions,images-networks,orchestration,user-actions,machines,monitoring-locally,keys,scripts,zones,rbac-teams misttests/gui/core/pr/features
}

run_api_tests_suite() {
    pytest_args=""
    for path in "${pytest_paths[@]}"
    do
      pytest_args="${pytest_args} ${path}"
    done
    pytest -s $pytest_args
}

run_provision_tests_suite() {
    python test_provisioning.py
}

vault_login() {
    if [ -z "$VAULT_CLIENT_TOKEN" ]
    then
        export vault_server=${VAULT_ADDR:-https://vault.ops.mist.io:8200}
        echo Vault username:
        read username
        echo Vault password:
        read -s password
        export PYTHONIOENCODING=utf8
        VAULT_CLIENT_TOKEN=$(curl $vault_server/v1/auth/userpass/login/$username -d '{ "password": "'${password}'" }' |
         python -c "import sys, json; print(json.load(sys.stdin)['auth']['client_token'])")

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

    declare -A pytest_paths

    pytest_paths["clouds"]='misttests/api/io/clouds.py'
    pytest_paths["images"]='misttests/api/io/images.py'
    pytest_paths["libcloud"]='misttests/api/io/libcloud_1.py misttests/api/io/libcloud_2.py'
    pytest_paths["machines"]='misttests/api/io/machines.py'
    pytest_paths["networks"]='misttests/api/io/networks.py'
    pytest_paths["keys"]='misttests/api/io/keys.py'
    pytest_paths["dns"]='misttests/api/io/dns.py'
    pytest_paths["scripts"]='misttests/api/io/scripts.py'
    pytest_paths["api_token"]='misttests/api/io/api_token.py'
    pytest_paths["schedules"]='misttests/api/io/schedules.py'
    pytest_paths["tunnels"]='misttests/api/core/tunnels.py'
    pytest_paths["orchestration"]='misttests/api/core/orchestration.py'
    pytest_paths["rbac"]='misttests/api/io/rbac.py'

    declare -A behave_tags

    behave_tags["clouds"]='clouds-add-1,'
    behave_tags["clouds-actions"]='clouds-actions,'
    behave_tags["images"]='images-networks,'
    behave_tags["keys"]='keys,'
    behave_tags["scripts"]='scripts','scripts-actions,'
    behave_tags["machines"]='machines,'
    behave_tags["users"]='user-actions,'
    behave_tags["rbac"]='rbac-teams,'
    behave_tags["schedules"]='schedulers-1','schedulers-2,'
    behave_tags["monitoring"]='monitoring-locally,'
    behave_tags["orchestration"]='orchestration,'
    behave_tags["rbac-rules"]='rbac-rules-1,'
    behave_tags["zones"]='zones,'


    if [ "$#" -eq 0 ]
    then
        vault_login
        run_api_tests_suite
        run_gui_tests_suite
    fi

    if [ $1 == '-h' ] || [ "$#" -gt 3 ]
    then
        help_message
        exit
    fi

    if [ "$#" -eq 1 ]
    then
        if [ $1 == '-api' ]
        then
            vault_login
            run_api_tests_suite
        elif [ $1 == '-gui' ]
        then
            vault_login
            run_gui_tests_suite
        elif [ $1 == '-provision' ]
        then
            vault_login
            run_provision_tests_suite
        elif [ $1 == '-t' ]
        then
            export VAULT_ENABLED=False
            run_api_tests_suite
            run_gui_tests_suite
        else
            help_message
        fi
    fi

    if [ "$#" -eq 2 ]
    then
        if [ $1 == '-t' ]
        then
            if [ $2 == '-api' ]
            then
                export VAULT_ENABLED=False
                run_api_tests_suite
            elif [ $2 == '-gui' ]
            then
                export VAULT_ENABLED=False
                run_gui_tests_suite
            else
                help_message
            fi
        elif [ $1 == '-api' ] && [[ " ${!pytest_paths[@]} " == *" $2 "* ]]; then
            vault_login
            pytest -s ${pytest_paths["$2"]}
        elif [ $1 == '-gui' ] && [[ " ${!behave_tags[@]} " == *" $2 "* ]]; then
            vault_login
            behave -k --no-capture --no-capture-stderr --stop --tags=${behave_tags["$2"]} misttests/gui/core/pr/features
       else

            help_message
        fi
    fi

    if [ "$#" -eq 3 ]
    then
        if [ $1 != '-t' ]
        then
            help_message
            exit
        fi
        export VAULT_ENABLED=False
        if [ $2 == '-api' ] && [[ " ${!pytest_paths[@]} " == *" $3 "* ]]; then
            pytest -s ${pytest_paths["$3"]}
        elif [ $2 == '-gui' ] && [[ " ${!behave_tags[@]} " == *" $3 "* ]]; then
            behave -k --no-capture --no-capture-stderr --stop --tags=${behave_tags["$3"]} misttests/gui/core/pr/features
        else
            help_message
        fi
    fi

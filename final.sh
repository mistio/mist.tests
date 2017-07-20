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
}

run_gui_tests_suite() {
    behave_tags=""
    for tag in "${behave_tags[@]}"
    do
      behave_tags+="${tag}"
    done
    behave -k --no-capture --no-capture-stderr --tags=$behave_tags misttests/gui/core/pr/features
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

    declare -A behave_tags

    behave_tags["clouds"]='clouds-add-1','clouds-add-2'
    behave_tags["clouds-actions"]='clouds-actions,'
    behave_tags["images"]='images-networks,'
    behave_tags["keys"]='keys,'
    behave_tags["scripts"]='scripts','scripts-actions'
    behave_tags["machines"]='machines,'
    behave_tags["users"]='user-actions,'
    behave_tags["rbac"]='rbac-teams'
    behave_tags["schedules"]='schedulers-1','schedulers-2,'
    behave_tags["monitoring"]='monitoring-locally'
    behave_tags["orchestration"]='orchestration,'
    behave_tags["rbac-rules"]='rbac-rules-1',



if [ "$#" -eq 0 ]
then
    vault_login
    run_api_tests_suite
    run_gui_tests_suite
else
    while getopts ":ha:g:" opt; do
        case $opt in
            a ) echo "Api arguments are = $OPTARG "
                set -f # disable glob
                IFS=',' # split on comma
                api_args=($OPTARG) ;; # use the split+glob operator
            g ) echo "Gui arguments are = $OPTARG"
                set -f # disable glob
                IFS=',' # split on comma
                gui_args=($OPTARG) ;; # use the split+glob operator
            h ) help_message ;;
            * ) help_message
                exit 1
        esac
    done
fi

if [ ${#api_args[@]} -ne 0 ]
then
    vault_login
    echo "Api arguments: ${#api_args[@]}"
    run_api_tests_suite
    pytest_args=""
    for arg in "${api_args[@]}"
    do
      if [ -n "${pytest_paths["$arg"]}" ]   # check if arg given exists
      then
        if [ -z "$pytest_args" ]
        then
            echo "First time!"
            pytest_args=${pytest_paths["$arg"]}
            echo "After first time:"
            echo $pytest_args
         else
            echo "Second time!"
            pytest_args="${pytest_args} ${pytest_paths["$arg"]}"
            echo $pytest_args
         fi
      else
        help_message
        exit
      fi
    done
    #run_api_tests_suite
    #pytest -s $pytest_args
    echo $pytest_args

fi

if [ ${#gui_args[@]} -ne 0 ]
then
    vault_login
    echo "Gui arguments: ${#gui_args[@]}"
fi

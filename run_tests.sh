#!/bin/bash

# fix key error

help_message() {
    echo "********************************************************************************************************************************"
    echo "********************************************************************************************************************************"
    echo "Usage: ./run_tests.sh [-t] [option] {argument}"
    echo "Options:"
    echo
    echo "[no option]   First API tests and then GUI tests will be invoked"
    echo "-h            Display this message"
    echo "-a            Run api tests suite. If no argument provided, the entire API tests suite will be invoked"
    echo "-g            Run gui tests suite. If no argument provided, the entire GUI tests suite will be invoked"
    echo "-provision    Run libcloud provision test."
    echo
    echo "Argument for API tests can be one of the following:"
    echo
    echo "clouds, machines, keys, dns, scripts, api_token, tunnels, schedules, orchestration, libcloud, networks, rbac, images"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, clouds-actions, machines, images, keys, scripts, users, rbac, schedules, orchestration, monitoring, rbac-rules, insights"
    echo "********************************************************************************************************************************"
    echo "********************************************************************************************************************************"
    echo
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

#        response=$(curl $vault_server/v1/auth/userpass/login/$username -d '{ "password": "'${password}'" }')

#        if [[ $response == *"errors"* ]]; then
#            echo 'Wrong credentials given...'
#            vault_login
#        else
#            echo $response
#            VAULT_CLIENT_TOKEN= "$("$response" | python -c "import sys, json; print(json.load(sys.stdin)['auth']['client_token'])")"
#            export VAULT_CLIENT_TOKEN
#            echo 'Successfully logged in. About to start running tests...'
#        fi
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
behave_tags["zones"]='zones,'

run_api_tests_suite() {
  pytest_args=""
  for path in "${pytest_paths[@]}"
  do
    pytest_args="${pytest_args} ${path}"
  done
  pytest $pytest_args || echo Failed
}

run_gui_tests_suite() {
  behave -o gui_test_suite_1_result.txt -k --no-capture --no-capture-stderr --tags=clouds-actions,images-networks,orchestration,scripts,scripts-actions,user-actions misttests/gui/core/pr/features || echo Failed
  behave -o gui_test_suite_2_result.txt -k --no-capture --no-capture-stderr --tags=keys,rbac-teams,zones misttests/gui/core/pr/features || echo Failed
  behave -o gui_test_schedules_result.txt -k --no-capture --no-capture-stderr --tags=schedulers-1,schedulers-2 misttests/gui/core/pr/features || echo Failed
  behave -o gui_test_rbac_rules_result.txt -k --no-capture --no-capture-stderr --tags=rbac-rules-1 misttests/gui/core/pr/features || echo Failed
  behave -o gui_test_rbac_rules_2_result.txt -k --no-capture --no-capture-stderr --tags=rbac-rules-2 misttests/gui/core/pr/features || echo Failed
  behave -o gui_test_machines_result.txt -k --no-capture --no-capture-stderr --tags=machines misttests/gui/core/pr/features || echo Failed
}

run_provision_tests_suite() {
    python test_provisioning.py || echo Failed
}

validate_api_args(){
  for arg in $@
  do
    if [ -z "${pytest_paths["$arg"]}" ]
    then
      echo "Wrong parameter has been given!"
      help_message
    fi
  done
}

validate_gui_args(){
  for arg in $@
  do
    if [ -z "${behave_tags["$arg"]}" ]
    then
      echo "Wrong parameter has been given!"
      help_message
    fi
  done
}

if [ "$#" -eq 0 ]
then
    vault_login
    run_api_tests_suite || echo Failed
    run_gui_tests_suite || echo Failed
fi

if [ "$#" -eq 1 ]
then
    if [ $1 == '-a' ]
    then
        vault_login
        run_api_tests_suite || echo Failed
    elif [ $1 == '-g' ]
    then
        vault_login
        run_gui_tests_suite || echo Failed
    elif [ $1 == '-p' ]
    then
        vault_login
        run_provision_tests_suite || echo Failed
    fi
else
  while getopts ":a:g:" opt; do
    case $opt in
      a)
        IFS=','
        echo "Api tests will be triggered. Parameters are: $OPTARG"
        if [ -z "$OPTARG" ]
        then
          vault_login
          run_api_tests_suite || echo Failed
        else
          validate_api_args "$OPTARG"
          vault_login
          for arg in $OPTARG
          do
              pytest ${pytest_paths["$arg"]} || echo Failed
          done
        fi
        ;;
      g)
        IFS=','
        echo "Gui tests will be triggered. Parameters are: $OPTARG"
        if [ -z "$OPTARG" ]
        then
          run_gui_tests_suite || echo Failed
        else
          validate_gui_args "$OPTARG"
          vault_login
          for arg in $OPTARG
          do
              behave -k --no-capture --no-capture-stderr --stop --tags=${behave_tags["$arg"]} misttests/gui/core/pr/features || echo Failed
          done
        fi
        ;;
     \?)
        echo "Invalid option: -$OPTARG" >&2
        help_message
        exit
        ;;
     :)
        echo nothing
        ;;
    esac
  done
fi

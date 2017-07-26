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
  echo "Running entire api tests suite..."
  pytest_args=""
  for path in "${pytest_paths[@]}"
  do
    pytest_args="${pytest_args} ${path}"
  done
  pytest $pytest_args
}

run_gui_tests_suite() {
    behave_tags=""
    for tag in "${behave_tags[@]}"
    do
      behave_tags+="${tag}"
    done
    behave -k --no-capture --no-capture-stderr --tags=$behave_tags misttests/gui/core/pr/features
}

validate_api_args(){
  for arg in $@
  do
    if [ -z "${pytest_paths["$arg"]}" ]
    then
      help_message
      exit
    fi
  done
}

validate_gui_args(){
  for arg in $@
  do
    if [ -z "${behave_tags["$arg"]}" ]
    then
      help_message
      exit
    fi
  done
}

while getopts ":a:g:" opt; do
  case $opt in
    a)
      IFS=','
      echo "Api tests will be triggered. Parameters are: $OPTARG"
      if [ -z "$OPTARG" ]
      then
        run_api_tests_suite
      else
        validate_api_args "$OPTARG"
        for arg in $OPTARG
        do
            pytest ${pytest_paths["$arg"]}
        done
      fi
      ;;
    g)
      IFS=','
      echo "Gui tests will be triggered. Parameters are: $OPTARG"
      if [ -z "$OPTARG" ]
      then
        run_gui_tests_suite
      else
        validate_gui_args "$OPTARG"
        for arg in $OPTARG
        do
            behave -k --no-capture --no-capture-stderr --stop --tags=${behave_tags["$arg"]} misttests/gui/core/pr/features
        done
      fi
      ;;
   \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
   :)
      echo nothing
      ;;
  esac
done

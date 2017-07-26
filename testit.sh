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
    echo "clouds, machines, keys, dns, scripts, api_token, tunnels, schedules, orchestration, libcloud, networks, rbac, images"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, clouds-actions, machines, images, keys, scripts, users, rbac, schedules, orchestration, monitoring, rbac-rules, insights"
    echo
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
  pytest $pytest_args
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

while getopts ":a:" opt; do
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
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      run_api_tests_suite
      #echo "Option -$OPTARG requires an argument." >&2
      #exit 1
      ;;
  esac
done

#!/bin/bash

help_message() {
    echo
    echo "Usage: ./run_tests.sh [option] {argument}"
    echo
    echo "-h     Display this message"
    echo "-api   Run api tests suite"
    echo "-gui   Run gui tests suite"
    echo
    exit
}


run_api_suite() {
    for path in "${!pytest_paths[@]}"; do echo "${pytest_paths[$path]}"; done
}


    declare -A pytest_paths

    pytest_paths["clouds"]='src/mist.io/tests/misttests/api/io/clouds.py'
    pytest_paths["images"]='src/mist.io/tests/misttests/api/io/images.py'
    pytest_paths["machines"]='src/mist.io/tests/misttests/api/io/machines.py'
    pytest_paths["keys"]='src/mist.io/tests/misttests/api/io/keys.py'
    pytest_paths["scripts"]='src/mist.io/tests/misttests/api/io/scripts.py'
    pytest_paths["tunnels"]='src/mist.io/tests/misttests/api/io/tunnels.py'
    pytest_paths["api_token"]='src/mist.io/tests/misttests/api/io/api_token.py'
    pytest_paths["schedules"]='src/mist.io/tests/misttests/api/io/schedules.py'

    declare -a arr=("clouds" "machines" "keys" "scripts" "tunnels")



    if [ $# -eq 0 ] || [ $1 == '-h' ]
    then
        help_message
        exit
    fi

    if [ "$#" -lt 2 ]
    then
        if [ $1 == '-api' ]
        then
            pytest_args=""
            for path in "${pytest_paths[@]}"
            do
              pytest_args="${pytest_args} ${path}"
            done
            pytest -s $pytest_args
            exit
        else
            help_message
        fi
    else
       if [ $1 == '-api' ] && [[ " ${!pytest_paths[@]} " == *" $2 "* ]]; then
            pytest -s ${pytest_paths["$2"]}
       else
            help_message
       fi
    fi

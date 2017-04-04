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

    declare -A pytest_paths

    pytest_paths["clouds"]='src/mist.io/tests/misttests/api/io/clouds.py'
    pytest_paths["images"]='src/mist.io/tests/misttests/api/io/images.py'
    pytest_paths["machines"]='src/mist.io/tests/misttests/api/io/machines.py'
    pytest_paths["keys"]='src/mist.io/tests/misttests/api/io/keys.py'
    pytest_paths["scripts"]='src/mist.io/tests/misttests/api/io/scripts.py'
    pytest_paths["tunnels"]='src/mist.io/tests/misttests/api/io/tunnels.py'
    pytest_paths["api_token"]='src/mist.io/tests/misttests/api/io/api_token.py'
    pytest_paths["schedules"]='src/mist.io/tests/misttests/api/io/schedules.py'

    if [ $# -eq 0 ] || [ $1 == '-h' ]
    then
        help_message
        exit
    fi

    if [ $1 == '-api']
    then

    fi
    

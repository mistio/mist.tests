#!/bin/bash

help_message() {
    echo
    echo "Usage: ./run_tests.sh [option] {argument}"
    echo
    echo "Options:"
    echo
    echo "-h     Display this message"
    echo "-api   Run api tests suite. If no argument provided, the entire API tests suite will be invoked"
    echo "-gui   Run gui tests suite"
    echo
    echo "Argument for API tests can be one of the following:"
    echo
    echo "clouds, machines, tunnels, keys, scripts, api_token, tunnels, schedules"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, machines, images, keys, scripts, users, rbac, schedules, orchestration"
    echo
    exit
}

ui_error_message() {
    echo
    echo 'For UI tests you have to specify the suite you want to run!'
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, machines, images, keys, scripts, users, rbac, schedules, orchestration"
    echo
}


run_api_tests_suite() {
    pytest_args=""
    for path in "${pytest_paths[@]}"
    do
      pytest_args="${pytest_args} ${path}"
    done
    pytest -s $pytest_args
}


    declare -A pytest_paths

    pytest_paths["clouds"]='misttests/api/io/clouds.py'
    pytest_paths["images"]='misttests/api/io/images.py'
    pytest_paths["machines"]='misttests/api/io/machines.py'
    pytest_paths["keys"]='misttests/api/io/keys.py'
    pytest_paths["scripts"]='misttests/api/io/scripts.py'
    pytest_paths["tunnels"]='misttests/api/io/tunnels.py'
    pytest_paths["api_token"]='misttests/api/io/api_token.py'
    pytest_paths["schedules"]='misttests/api/io/schedules.py'

    declare -A behave_tags

    behave_tags["clouds"]='clouds-add-a','clouds-add-b','clouds-actions'
    behave_tags["images"]='images-networks'
    behave_tags["keys"]='keys'
    behave_tags["scripts"]='scripts'
    behave_tags["machines"]='machines'
    behave_tags["users"]='user-actions'
    behave_tags["rbac"]='rbac-rules','rbac-teams'
    behave_tags["schedules"]='schedulers','schedulers_v2'
    behave_tags["orchestration"]='orchestration'


    if [ "$#" -eq 0 ] || [ $1 == '-h' ] || [ "$#" -gt 2 ]
    then
        help_message
        exit
    fi

    if [ "$#" -lt 2 ]
    then
        if [ $1 == '-api' ]
        then
            run_api_tests_suite
            exit
        elif [ $1 == '-gui' ]
        then
            ui_error_message
        else
            help_message
        fi
    else
       if [ $1 == '-api' ] && [[ " ${!pytest_paths[@]} " == *" $2 "* ]]; then
            pytest -s ${pytest_paths["$2"]}
       elif [ $1 == '-gui' ] && [[ " ${!behave_tags[@]} " == *" $2 "* ]]; then
            behave -k --stop --tags=${behave_tags["$2"]} misttests/gui/core/pr/features
       else
            help_message
       fi
    fi

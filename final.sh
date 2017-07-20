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
            #graceful_exit ;;
        * ) usage
            clean_up
            exit 1
    esac
done

echo "Api arguments: ${#api_args[@]}"
echo "Gui arguments: ${#gui_args[@]}"

#echo -n "Arguments are:"
#for i in "${array[@]}"; do
#  echo -n " ${i} "
#done

printf "\b \n"

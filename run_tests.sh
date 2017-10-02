#!/bin/bash

declare -A pytest_paths

pytest_paths["clouds"]='misttests/api/io/clouds.py'
pytest_paths["images"]='misttests/api/io/images.py'
pytest_paths["libcloud1"]='misttests/api/io/libcloud_1.py'
pytest_paths["libcloud2"]='misttests/api/io/libcloud_2.py'
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
#pytest_paths["ip-whitelisting"]='misttests/api/io/ip_whitelisting.py'

declare -A behave_tags

behave_tags["clouds"]='clouds-add-1'
behave_tags["clouds-actions"]='clouds-actions'
behave_tags["images"]='images-networks'
behave_tags["keys"]='keys'
behave_tags["scripts"]='scripts','scripts-actions'
behave_tags["machines"]='machines'
behave_tags["users"]='user-actions'
behave_tags["rbac"]='rbac-teams'
behave_tags["schedules"]='schedulers-1','schedulers-2'
behave_tags["monitoring"]='monitoring-locally'
behave_tags["orchestration"]='orchestration'
behave_tags["rbac-rules"]='rbac-rules-1'
behave_tags["zones"]='zones'
behave_tags["insights"]='insights'
#behave_tags["ip-whitelisting"]='ip-whitelisting'


help_message() {
    echo "********************************************************************************************************************************"
    echo "********************************************************************************************************************************"
    echo "Usage: ./run_tests.sh [option] {<arg1>},{<arg2>},..."
    echo "Options:"
    echo
    echo "[no option]   First API tests and then GUI tests will be invoked"
    echo "-h            Display this message"
    echo "-a            Run api tests suite. If no argument provided, the entire API tests suite will be invoked"
    echo "-g            Run gui tests suite. If no argument provided, the entire GUI tests suite will be invoked"
    echo "-p            Run libcloud provision test."
    echo "-c            Continue after failures without providing an interactive postmortem"
    echo
    echo "Argument for API tests can be one of the following:"
    echo
    echo "clouds, machines, tunnels, keys, dns, scripts, api_token, tunnels, schedules, orchestration, libcloud1, libcloud2, networks, rbac, ip-whitelisting"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, clouds-actions, machines, images, keys, scripts, users, rbac, schedules, orchestration, monitoring, rbac-rules, insights, ip-whitelisting"
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

        VAULT_CLIENT_TOKEN=$(
          curl -k $vault_server/v1/auth/userpass/login/$username -d '{ "password": "'${password}'" }' |
          python -c "
import sys, json;
res = json.load(sys.stdin)
if res.get('auth'):
    print(res['auth']['client_token'])"
        )

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


run_api_tests_suite() {
    test_suite_paths=""
    for suite in $suites
    do
        if [ -z "${pytest_paths["$suite"]}" ]; then
            #echo "No api tests available for $suite"
            continue
        else
            test_suite_paths="${test_suite_paths} ${pytest_paths["$suite"]}"
        fi
    done
    if [ "${test_suite_paths}" == "" ]; then
        echo "No api tests available for $suites"
    else
        time parallel --no-notice --fg --tmuxpane /mist.core/mist.io/tests/wrapper.sh api $datadir $break_on_failure ::: $test_suite_paths
    fi
}


run_gui_tests_suite() {
    test_suite_paths=""
    for suite in $suites
    do
        if [ -z "${behave_tags["$suite"]}" ]; then
            continue
        else
            test_suite_paths="${test_suite_paths} ${behave_tags["$suite"]}"
        fi
    done
    if [ "${test_suite_paths}" == "" ]; then
        echo "No gui tests available for $suite"
    else
        time parallel -j 1 --no-notice --fg --tmuxpane /mist.core/mist.io/tests/wrapper.sh gui $datadir $break_on_failure ::: $test_suite_paths
    fi
}


run_provision_tests_suite() {
    python test_provisioning.py || echo Failed
}


validate_suites(){
    for arg in $suites
    do
        if [ -z "${pytest_paths["$arg"]}" ] && [ -z "${behave_tags["$arg"]}" ]
        then
            echo "Invalid test suite: $arg"
            help_message
            exit 112
        fi
    done
}


# Initialize
run_api_tests=0
run_gui_tests=0
login_only=0
break_on_failure=1

for i in "$@"
do
case $i in
    -a|--api)
    run_api_tests=1
    shift
    ;;
    -g|--gui)
    run_gui_tests=1
    shift
    ;;
    -c)
    break_on_failure=0
    shift
    ;;
    -l)
    login_only=1
    shift
    ;;
    -h|--help)
    help_message
    exit 0
    ;;
esac
done

suites=$@

# If no suites are given
if [ "$suites" == "" ]; then
    for suite in "${!pytest_paths[@]}"
    do
        suites="${suites} ${suite}"
    done
    for suite in "${!behave_tags[@]}"
    do
        if [[ "$suites" == *"$suite"* ]]; then
            continue
        fi
        suites="${suites} ${suite}"
    done
fi

validate_suites

datadir=/data/`date '+%Y_%m_%d_%H_%M_%S'`
mkdir -p $datadir

vault_login

if [ $login_only -eq 1 ]; then
    exit 0
fi

if [ $run_api_tests -eq 0 ] && [ $run_gui_tests -eq 0 ]; then
  run_api_tests=1
  run_gui_tests=1
fi


if [ $run_api_tests -eq 1 ]; then
    echo "Running API tests suites: $suites"
    run_api_tests_suite
fi
if [ $run_gui_tests -eq 1 ]; then
    echo "Running GUI tests suites: $suites"
    run_gui_tests_suite
fi

failed=$(ls $datadir)
failed_count=$(ls $datadir.txt|wc -w)

if [ "$failed_count" == "0" ]; then
    echo "All tests passed!"
else
    echo $failed_count suites failed: $failed
    echo "Show details? [Y/n]"
    read response
    if [ "$response" == "n" ]; then
        exit 0
    else
        cd $datadir
        less *.txt
        cd -
    fi
fi
echo "Logs are available at $datadir"

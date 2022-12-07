#!/bin/bash

declare -A pytest_paths

pytest_paths["buckets"]='misttests/integration/api/main/buckets.py'
pytest_paths["secrets"]='misttests/integration/api/main/secrets.py'
pytest_paths["clouds"]='misttests/integration/api/main/clouds.py'
pytest_paths["images"]='misttests/integration/api/main/images.py'
pytest_paths["libcloud1"]='misttests/integration/api/main/libcloud_1.py'
pytest_paths["libcloud2"]='misttests/integration/api/main/libcloud_2.py'
pytest_paths["machines"]='misttests/integration/api/main/machines.py'
pytest_paths["networks"]='misttests/integration/api/main/networks.py'
pytest_paths["keys"]='misttests/integration/api/main/keys.py'
pytest_paths["dns"]='misttests/integration/api/main/dns.py'
pytest_paths["scripts"]='misttests/integration/api/main/scripts.py'
pytest_paths["api_token"]='misttests/integration/api/main/api_token.py'
pytest_paths["schedules"]='misttests/integration/api/main/schedules.py'
pytest_paths["teams"]='misttests/integration/api/main/teams.py'
pytest_paths["ip-whitelisting"]='misttests/integration/api/main/ip_whitelisting.py'
pytest_paths["tunnels"]='misttests/integration/api/plugin/tunnels.py'
pytest_paths["orchestration"]='misttests/integration/api/plugin/orchestration.py'
pytest_paths["endpoints"]='misttests/integration/api/main/cloud_endpoints.py'

pytest_paths["orgs-v2"]='misttests/integration/api/main/v2/test_orgs_controller.py'
pytest_paths["clouds-v2"]='misttests/integration/api/main/v2/test_clouds_controller.py'
pytest_paths["jobs-v2"]='misttests/integration/api/main/v2/test_jobs_controller.py'
pytest_paths["snapshots-v2"]='misttests/integration/api/main/v2/test_snapshots_controller.py'
pytest_paths["zones-v2"]='misttests/integration/api/main/v2/test_zones_controller.py'
pytest_paths["snapshots-v2"]='misttests/integration/api/main/v2/test_snapshots_controller.py'
pytest_paths["machines-v2-1"]='misttests/integration/api/main/v2/test_machines_controller_1.py'
pytest_paths["machines-v2-2"]='misttests/integration/api/main/v2/test_machines_controller_2.py'
pytest_paths["machines-v2-3"]='misttests/integration/api/main/v2/test_machines_controller_3.py'
declare -A behave_tags

behave_tags["clouds-add-1"]='clouds-add-1'
behave_tags["clouds-add-2"]='clouds-add-2'
behave_tags["clouds-actions"]='clouds-actions'
behave_tags["images"]='images-networks'
behave_tags["keys"]='keys'
behave_tags["scripts"]='scripts','scripts-actions'
behave_tags["machines-1"]='machines-1'
behave_tags["machines-2"]='machines-2'
behave_tags["rules-1"]='rules-1'
behave_tags["rules-2"]='rules-2'
behave_tags["rules-3"]='rules-3'
behave_tags["users"]='user-actions'
behave_tags["teams"]='teams'
behave_tags["schedules-1"]='schedulers-1'
behave_tags["schedules-2"]='schedulers-2'
behave_tags["schedulers-script"]='schedulers-script'
behave_tags["ip-whitelisting"]='ip-whitelisting'

behave_tags["monitoring"]='monitoring'
behave_tags["orchestration"]='orchestration'
behave_tags["rbac-1"]='rbac-1'
behave_tags["rbac-2"]='rbac-2'
behave_tags["rbac-3"]='rbac-3'
behave_tags["rbac-4"]='rbac-4'
behave_tags["zones"]='zones'
behave_tags["insights"]='insights'
behave_tags["pricing"]='pricing'


help_message() {
    echo "********************************************************************************************************************************"
    echo "********************************************************************************************************************************"
    echo "Usage: ./run_tests.sh [option] {<arg1>},{<arg2>},..."
    echo "Options:"
    echo
    echo "[no option]   First API tests and then GUI tests will be invoked"
    echo "-h            Display this message"
    echo "-t            Skip Vault login"
    echo "-a            Run api tests suite. If no argument provided, the entire API tests suite will be invoked"
    echo "-g            Run gui tests suite. If no argument provided, the entire GUI tests suite will be invoked"
    echo "-p            Run libcloud provision test."
    echo "-c            Continue after failures without providing an interactive postmortem"
    echo
    echo "Argument for API tests can be one of the following:"
    echo
    echo "clouds, machines, tunnels, keys, dns, scripts, api_token, tunnels, schedules, orchestration, libcloud1, libcloud2, networks, teams, ip-whitelisting"
    echo
    echo "Argument for UI tests can be one of the following:"
    echo
    echo "clouds, clouds-actions, machines, images, keys, scripts, users, teams, schedules, orchestration, monitoring, rbac-1, rbac-2, rbac-3, rbac-4, insights, zones, ip-whitelisting, endpoints"
    echo
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
        time /mist.tests/wrapper.sh api $datadir $break_on_failure $test_suite_paths
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
        pkill -9 chrom
        if [ -z "$VNC" ]
        then  # Headless mode, run tests in parallel
            time parallel --no-notice --fg --tmuxpane /mist.tests/wrapper.sh gui $datadir $break_on_failure ::: $test_suite_paths
        else  # VNC mode, run tests serially
            /mist.tests/wrapper.sh gui $datadir $break_on_failure $test_suite_paths
        fi
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
skip_vault=0
run_api_tests=0
run_gui_tests=0
login_only=0
break_on_failure=1

for i in "$@"
do
case $i in
    -t)
    skip_vault=1
    shift
    ;;
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

if [ $skip_vault -eq 0 ]; then
    source ./vault_login.sh
fi

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

failed=$(ls $datadir/*.txt)
failed_count=$(ls $datadir/*.txt  2>/dev/null|wc -w)

if [ "$failed_count" == "0" ]; then
    echo "All tests passed!"
else
    echo $failed_count suites failed: $failed
    echo "Show details? [Y/n]"
    read response
    if [ "$response" == "n" ]; then
        exit 0
    else
        cat $datadir/*.txt | more
    fi
fi
echo "Logs are available at $datadir"

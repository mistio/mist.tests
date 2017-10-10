#!/bin/bash
test_type=$1
datadir=$2
break_on_failure=$3

if [ "${test_type}" == "api" ]; then
    suite=`echo $4 | rev |cut -d "/" -f1 | rev | cut -d "." -f1`

    if [ "${break_on_failure}" == "1" ]; then
        ipdb="--ipdb"
    else
        ipdb=""
    fi
    cmd="/usr/local/bin/pytest $ipdb /mist.core/mist.io/tests/$4"
else
    suite=$4
    cd misttests/gui/core/pr/features/
    export BEHAVE_DEBUG_ON_ERROR=$3
    export DATADIR=$2
    cmd="/usr/local/bin/behave -k --no-capture --no-capture-stderr --stop --tags=$4"
fi

logfile=$datadir/${test_type}-${suite}.txt
script -e -c "$cmd" $logfile
ret=${PIPESTATUS[0]}

if [ $ret -ne 0 ]; then
    echo $cmd failed with exit code $ret
    echo logs available at $logfile
    # read -p "Press enter to continue" input
else
    # echo $cmd succeeded with exit code $ret
    # echo logs available at $logfile
    # read -p "Press enter to continue" input
    rm $logfile
fi

exit $ret

#!/bin/bash
test_type=$1
datadir=$2
break_on_failure=$3

if [ "${test_type}" == "api" ]; then
    cmd="/usr/local/bin/pytest /mist.core/mist.io/tests/$4"
    suite=`echo $4 | rev |cut -d "/" -f1 | rev | cut -d "." -f1`
else
    cd misttests/gui/core/pr/features/
    export BEHAVE_DEBUG_ON_ERROR=$3
    export DATADIR=$2
    cmd="/usr/local/bin/behave -k --tags=$4"
    suite=$4
fi

logfile=$datadir/${suite}-${test_type}.txt

if [ "${break_on_failure}" == "1" ]; then
    script -e -c "$cmd" $logfile
    ret=$?
else
    tee -a $logfile | $cmd | tee -a $logfile
    ret=${PIPESTATUS[1]}
fi

if [ $ret -ne 0 ]; then
    if [ "${break_on_failure}" == "1" ]; then
        echo $cmd failed with exit code $ret
        read -p "Press enter to continue" input
    fi
else
    rm $logfile
fi

exit $ret
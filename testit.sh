#!/bin/bash

declare -A pytest_paths

pytest_paths["clouds"]='misttests/api/io/clouds.py'
pytest_paths["images"]='misttests/api/io/images.py'
pytest_paths["libcloud"]='misttests/api/io/libcloud_1.py misttests/api/io/libcloud_2.py'
pytest_paths["machines"]='misttests/api/io/machines.py'

while getopts ":a:" opt; do
  case $opt in
    a)
      IFS=','
      echo "-a was triggered, Parameter: $OPTARG"
      for arg in $OPTARG
      do
        echo $arg
        sleep .5
        if [ -n "${pytest_paths["$arg"]}" ]   # check if arg given exists
        then
          echo $arg
          #echo ${pytest_paths["$arg"]}
          #pytest_args="${pytest_args} ${pytest_paths["$arg"]}"
          #echo $pytest_args
          pytest ${pytest_paths["$arg"]}
          #pytest -s $pytest_args
        fi
      done
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

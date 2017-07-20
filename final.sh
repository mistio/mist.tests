#!/bin/bash

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
        h ) helptext
            graceful_exit ;;
        * ) usage
            clean_up
            exit 1
    esac
done

echo "Number of arguments: ${#array[@]}"
echo -n "Arguments are:"
for i in "${array[@]}"; do
  echo -n " ${i} "
done
printf "\b \n"

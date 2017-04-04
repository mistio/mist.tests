#!/bin/bash

help_message() {
    echo "Usage: ./run_tests.sh [option] {argument}"
    echo
    echo "[no option]: Display this message"

    echo "[LOCAL DEV options]"
    echo "-h Show this message"
    echo "-l Will not download newer images and start docker-compose with what exists locally"
    echo "-m Will not mount code inside the containers"
    echo "-u If on linux and want to use unison instead of docker mount"
    echo "-t Will start the tests_base container. By default you will able to open a vncviewer/client"
    echo "   to localhost:5900"
    echo "-c Cleanup of old containers and images. Saves space in disk"
    echo "-d Destroy docker-compose stack. I will cleanup previous containers and stop the compose environment"
    echo
    echo "[DEBUG TOOLS options]"
    echo "-g GRAFANA: Will port-forward dogfood's grafana to localhost:3000"
    echo "-r {tesla|dogfood} RABBITMQ_MANAGEMENT: Will port-forward tesla/dogfood rabbitmq_management to"
    echo "                   localhost:15672"
    exit
}

    if [ $# -eq 0 ] || [ $1 == '-h' ]
    then
        help_message
    fi


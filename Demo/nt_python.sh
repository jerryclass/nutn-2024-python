#!/bin/bash

command=$1

IMAGE_NAME="nutn-my-python"
if [ "$command" = "init" ]; then
    if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
        echo "Docker image $IMAGE_NAME not found. Building..."
        docker build -f Docker/Dockerfile -t $IMAGE_NAME .
    fi
    docker build -f Docker/Dockerfile -t $IMAGE_NAME .
fi
    
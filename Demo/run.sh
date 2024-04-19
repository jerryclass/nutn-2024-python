#!/bin/bash

IMAGE_NAME="nutn-my-python"

if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
	echo "Docker image $IMAGE_NAME not found. Building..."
	docker build -f Docker/Dockerfile -t $IMAGE_NAME .
fi

docker run -it --rm -v "$(pwd):/app" $IMAGE_NAME python /app/get_data.py
#!/bin/bash

IMAGE_NAME="nutn-my-postgres"
command=$1

if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
	echo "Docker image $IMAGE_NAME not found. Building..."
	docker build -f Postgres/Dockerfile -t $IMAGE_NAME .
fi

# check docker container is exist
if docker ps -a --format '{{.Names}}' | grep -q 'nutn-my-postgres-container'; then
    echo "Container exists"
else
    echo "Container does not exist"
	docker run --name nutn-my-postgres-container -d $IMAGE_NAME
fi

if [ "$command" = "start" ]; then
	echo "start postgres services"
	docker start nutn-my-postgres-container
elif [ "$command" = "stop" ]; then
	echo "stop postgres services"
	docker stop nutn-my-postgres-container
else
	echo "command not found"
fi
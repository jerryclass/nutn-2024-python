#!/bin/bash

IMAGE_NAME="nutn-my-postgres"
command=$1

# check container is exist
check_container_exists() {
    if docker ps -a --format '{{.Names}}' | grep -q 'nutn-my-postgres-container'; then
        return 0
    else
        return 1
    fi
}

if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
	echo "Docker image $IMAGE_NAME not found. Building..."
	docker build -f Postgres/Dockerfile -t $IMAGE_NAME .
fi

if ! check_container_exists; then
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
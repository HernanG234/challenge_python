#!/bin/bash

: "${ENTRYPOINT=""}"
CMD=$1
service="challenge"

if [ "$ENTRYPOINT" == "" ]; then
    docker-compose run \
        -v "${PWD}":/app \
        ${service}
else
    if [ "$CMD" == "" ]; then
        docker-compose run \
            --entrypoint "${ENTRYPOINT}" \
            -v "${PWD}":/app \
            ${service}
    else
        docker-compose run \
        --entrypoint "${ENTRYPOINT}" \
        -v "${PWD}":/app \
        ${service} -c "$CMD"
    fi
fi

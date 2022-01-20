#!/bin/bash

TIME=$(date +'%T' | sed 's/:/_/g')
CONTAINER=$1
ID=$2

sudo docker run -v /local/repository/collectedData:/data --network=container:${CONTAINER} --name docker_tcpdump${ID} docker-tcpdump ' -v -w /data/${TIME}_${CONTAINER}.pcap'

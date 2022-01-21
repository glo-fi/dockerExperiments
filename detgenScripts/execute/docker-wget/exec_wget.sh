#!/bin/bash

IP=$1
ROUNDS=$2

sleep 60
counter=0
while [$counter < $ROUNDS]
do
    wget http://${IP}
    ((counter++))
done

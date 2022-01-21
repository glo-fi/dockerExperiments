#!/bin/sh

IP=$1
ROUNDS=$2

sleep 20
for ((i=1; i<ROUNDS; i++))
do
    wget http://${IP}:8080
done

#!/bin/bash

sudo docker run -dit --name docker-wget -v /local/repository/detgenScripts/execute/docker-wget:/local/scripts  docker-wget

sudo docker exec docker-wget /local/scripts/exec_wget.sh

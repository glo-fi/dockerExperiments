#!/bin/bash

sudo docker run -dit --name docker-httpd -p 8080:80 -v /local/repository/htdocs:/usr/local/apache2/htdocs/ httpd:2.4

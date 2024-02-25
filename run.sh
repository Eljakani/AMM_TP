#!/bin/bash

docker build -t multimedia .
docker run -d -p "5500:5000" --name multimedia multimedia
echo "Application link: http://localhost:5500"
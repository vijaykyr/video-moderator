#!/usr/bin/env bash
#delete old container (if applicable)
docker rm -f video_moderator
#build image
docker build -t gcr.io/vijays-sandbox/video-moderator:latest .
#create new container from image, bind host port 80 to container port 8081
docker run -dp 80:8081 --name=video_moderator gcr.io/vijays-sandbox/video-moderator:latest


#!/usr/bin/env bash
#build image
docker build -t gcr.io/vijays-sandbox/video-moderator:latest ..
#create new container from image, bind host port 80 to container port 8081
docker run --rm -itp 80:8081 --name=video_moderator gcr.io/vijays-sandbox/video-moderator:latest


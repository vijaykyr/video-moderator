#!/usr/bin/env bash
#clean existing containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

docker build -t gcr.io/vijays-sandbox/video-moderator:django .

docker run -itp 80:80 gcr.io/vijays-sandbox/video-moderator:django


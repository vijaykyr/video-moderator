#!/usr/bin/env bash
#change working directory to current directory
cd "$(dirname "$0")"

#grab project name
PROJECT=$(gcloud config list | grep project | cut -d ' ' -f3)

#build image
docker build -t gcr.io/$PROJECT/video-moderator:latest .

#push to gcr
gcloud docker push gcr.io/$PROJECT/video-moderator:latest

#Create cluster
gcloud container clusters create "video-moderator" --zone "us-central1-c" --machine-type "n1-standard-1" --num-nodes "3"

#Configure kubectl
gcloud container clusters get-credentials video-moderator

#Create deployment object
kubectl run video-moderator --image=gcr.io/$PROJECT/video-moderator:latest --port=80 --replicas=3

#Allow external traffic
kubectl expose deployment video-moderator --type="LoadBalancer"

#!/usr/bin/env bash
#grab project name
PROJECT = gcloud config list | grep project | cut -d ' ' -f3

#build image
docker build -t gcr.io/$PROJECT/video-moderator:latest .

#push to gcr
gcloud docker push gcr.io/$PROJECT/video-moderator:latest

#Create cluster
gcloud container clusters create "video-moderator" --zone "us-central1-c" --machine-type "n1-standard-1" --num-nodes "5"

#Configure kubectl
gcloud container clusters get-credentials video-moderator

#Deploy pods to cluster
kubectl run video-moderator --image=gcr.io/$PROJECT/video-moderator:latest --port=80 --replicas=5

#Allow external traffic
kubectl expose rc video-moderator --type="LoadBalancer"

#!/usr/bin/env bash
#build image
docker build -t gcr.io/vijays-sandbox/video-moderator:django .

#push to gcr
gcloud docker push gcr.io/vijays-sandbox/video-moderator:django

#Create cluster
gcloud container clusters create "video-moderator" --zone "us-central1-c" --machine-type "n1-standard-2" --num-nodes "3"

#Configure kubectl
gcloud container clusters get-credentials video-moderator

#Deploy pods to cluster
kubectl run video-moderator --image=gcr.io/vijays-sandbox/video-moderator:django --port=80 --replicas=3

#Allow external traffic
kubectl expose deployment video-moderator --type="LoadBalancer"

#!/usr/bin/env bash
#Create cluster

#build image
docker build -t gcr.io/vijays-sandbox/video-moderator:latest .

#push to gcr
gcloud docker push gcr.io/vijays-sandbox/video-moderator:latest

#Configure kubectl
gcloud container clusters get-credentials cluster-1

#Deploy pods to cluster
kubectl run video-moderator --image=gcr.io/vijays-sandbox/video-moderator:latest --port=8000 --replicas=5

#Allow external traffic
kubectl expose rc video-moderator --type="LoadBalancer"

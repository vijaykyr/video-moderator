#!/usr/bin/env bash
#delete external load balancer
kubectl delete services video-moderator

#Delete the running pods
kubectl delete deployment video-moderator

#Delete the cluster
gcloud container clusters delete video-moderator
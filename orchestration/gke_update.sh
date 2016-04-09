#!/usr/bin/env bash
#Usage: ./gke_update.sh version_number

#grab project name
PROJECT = gcloud config list | grep project | cut -d ' ' -f3

#update image
docker build -t gcr.io/$PROJECT/video-moderator:$1 .

#push to gcr
gcloud docker push gcr.io/$PROJECT/video-moderator:$1

#roll update to pods
kubectl rolling-update video-moderator --image=gcr.io/$PROJECT/video-moderator:$1 --update-period=1s
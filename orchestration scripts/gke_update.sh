#!/usr/bin/env bash

#Usage:
# ./gke_update.sh version_number

#update image
docker build -t gcr.io/vijays-sandbox/video-moderator:$1 ..

#push to gcr
gcloud docker push gcr.io/vijays-sandbox/video-moderator:$1

#roll update to pods
kubectl rolling-update video-moderator --image=gcr.io/vijays-sandbox/video-moderator:$1 --update-period=1s
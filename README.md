#Video Moderator

This README file is a work in progress. Instructions are not complete.

###What it is
A Django/Python app that processes mp4 videos, extracts still frames, and sends them to the Google Vision API
for moderation.

###How to deploy on Google Container Engine (GKE)
Note: Replace all references to 'PROJECT_ID' with your project ID before running commands

####Part 1: Build Docker image and push to Google Container Registry (GCR)
1. Build docker image. Run from command the same directory that contains the Dockerfile
`docker build -t gcr.io/PROJECT_ID/video-moderator:v1 .`
2. Push to GCR
`gcloud docker push gcr.io/PROJECT_ID/video-moderator:v1`

####Part 2: Spin up GKE cluster and deploy pod(s)
1. Create GKE cluster
2. [Configure kubectl](https://cloud.google.com/container-engine/docs/before-you-begin#optional_set_gcloud_defaults)
3. Deploy pods to cluster
`kubectl run video-moderator --image=gcr.io/PROJECT_ID/video-moderator:v1 --port=8000 --replicas=1`
4. Allow external traffic
`kubectl expose rc video-moderator --type="LoadBalancer"`

#Video Moderator

This README file is a work in progress. Instructions are not complete.

###What it is
A Django/Python app that processes mp4 videos, extracts still frames, and sends them to the Google Vision API
for moderation.

###How to build
From the same directory that contains the Dockerfile
`docker build -t gcr.io/<project-name>/video-moderator:v1 .`

###How to deploy on GKE
1) Create GKE cluster
2) Deploy pods to cluster
`kubectl run video-moderator --image=gcr.io/PROJECT_ID/video-moderator:v1 --port=8000`
3) Allow external traffic
`kubectl expose rc video-moderator --type="LoadBalancer"`

#Video Moderator

This README file is a work in progress. Instructions are not complete.

###What it is
A Django/Python app that processes mp4 videos, extracts still frames, and sends them to the Google Vision API
for moderation.

####How to deploy on Google Container Engine (GKE)
Note: Replace all references to 'PROJECT_ID' with your project ID before running commands

####Part 1: Build Docker image and push to Google Container Registry (GCR)
1. Build docker image. Run from command the same directory that contains the Dockerfile
`docker build -t gcr.io/PROJECT_ID/video-moderator:latest .`
2. Push to GCR
`gcloud docker push gcr.io/PROJECT_ID/video-moderator:latest`

####Part 2: Spin up GKE cluster and deploy pod(s)
1. Create GKE cluster
`gcloud container clusters create "video-moderator" --zone "us-central1-c"`
2. Configure kubectl
`gcloud container clusters get-credentials video-moderator`
3. Deploy pods to cluster
`kubectl run video-moderator --image=gcr.io/PROJECT_ID/video-moderator:latest --port=8000 --replicas=1`
4. Allow external traffic
`kubectl expose rc video-moderator --type="LoadBalancer"`
5. Determine external IP (this will take a minute to generate after the last command)
`kubectl get service video-moderator`
6. Paste <EXTERNAL_IP>:8000 into browser to access web app

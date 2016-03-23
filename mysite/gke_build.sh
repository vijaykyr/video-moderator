#build image
docker build -t gcr.io/vijays-sandbox/video-moderator:latest .

#push to gcr
gcloud docker push gcr.io/vijays-sandbox/video-moderator:latest

#roll update to pods
kubectl rolling-update video-moderator --image=gcr.io/vijays-sandbox/video-moderator:latest --update-period=1s
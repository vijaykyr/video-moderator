#Video Moderator

####What it is
A web service that processes mp4 videos, extracts still frames, and sends them to the Google Vision API
for moderation.

####Instructions to deploy to Google Container Engine (GKE)
1. Install Docker: https://docs.docker.com/engine/installation/
2. Install Google Cloud SDK (gcloud): https://cloud.google.com/sdk/downloads
3. Run `gcloud components install kubectl`
4. Run `gcloud init`
5. Run `orchestration/gke_deploy.sh`

####File descriptions
1. **vid_moderator.py**  
The main processing script that does the video extraction and interacts with the Google APIs (Vision and GCS)
2. **express_server.js**   
A webserver with a simple html form front end that wraps vid_moderator.py. Videos submitted  
through the form are handed off to vid_moderator.py for asyncronous non-blocking processing. You can also
submit processing requests API style with an HTTP GET request.
3. **orchestration/Dockerfile**   
Instructions for containerizing the application

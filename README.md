#Video Moderator

####What it is
A web service that processes mp4 videos, extracts still frames, and sends them to the Google Vision API
for moderation.

####How to deploy on Google Container Engine (GKE)
1. Install Docker. You will need this to build the docker image
2. Edit orchestration/gke_deploy.sh to reference your GCP project
3. 
```bash
orchestration/gke_deploy.sh
```

####Key file descriptions
1. **vid_moderator.py**  
The main processing script that does the video extraction and interacts with the Google APIs (Vision and GCS)
2. **express_server.js**   
A webserver with a simple html form front end that wraps vid_moderator.py. Videos submitted  
through the form are handed off to vid_moderator.py for asyncronous non-blocking processing. You can also
submit processing requests API style with an HTTP GET request.
3. **orchestration/Dockerfile**   
Contains instructions for containerizing application
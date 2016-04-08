#Build from nodejs slim image
FROM node:4.4.2-slim

# Install APT packages
RUN apt-get update && apt-get install -y \
    python2.7 \
    python-pip

RUN apt-get install --fix-missing -y python-opencv

# Install Google API python client
RUN pip install --upgrade google-api-python-client

#Copy local resources
RUN git clone https://github.com/vijaykyr/video-moderator.git /video_moderator

#Change working directory
WORKDIR /video_moderator

#Expose private port inside container (bind to public port N using 'docker run -p N:8081')
EXPOSE 8081
#Start web server
CMD ["node", "express_server.js"]

#Image size breakdown
# Total: 750MB
#  ~200MB Nodejs Base Image (includes debian linux)
#  ~200MB python-pip
#  ~190MB python-opencv
#  ~130MB Google API Client
#  ~30MB  python2.7
# Ideas to reduce image size
#  1) Can you install Google API client w/o pip?
#  2) Use lighterweight framegrabber than opencv
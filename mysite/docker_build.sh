#clean existing containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

docker build -t gcr.io/vijays-sandbox/video-moderator:latest .

docker run -itp 8000:8000 gcr.io/vijays-sandbox/video-moderator:latest


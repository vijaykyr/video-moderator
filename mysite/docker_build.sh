#stop existing containers
docker stop $(docker ps -a -q)

docker build -t gcr.io/vijays-sandbox/vid-mod:v1 .

docker run -itp 8000:8000 gcr.io/vijays-sandbox/vid-mod:v1

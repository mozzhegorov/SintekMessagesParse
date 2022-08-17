git pull origin
docker build -t sintekmessagesparse .
docker stop sintekmsgs
docker rm sintekmsgs
docker run --name sintekmsgs -p 5005:5000 -d --restart=always sintekmessagesparse

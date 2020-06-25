eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&


source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
docker stop griffin
docker rm griffin
docker rmi griffindeveloper/griffin:latest
docker run -d --name griffin -p 5000:5000 griffindeveloper/griffin:latest

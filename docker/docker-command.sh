## Docker Command

# run docker mongo bind mount port expose container
docker run -d --name mongo -p 27017:27017 -v "/host_mnt/d/Documents/Dockerfile/mongo/data/db:/data/db"  mongo:latest
## Docker Command

# run docker mongo bind mount port expose container
docker run -d --name mongo -p 27017:27017 -v "/host_mnt/d/Documents/Dockerfile/mongo/data/db:/data/db"  mongo:latest

# run docker python script
docker run -it --rm --name my-first-python-script -v /host_mnt/c/Users/mochamad/OneDrive/progressive/docker/docker-python/app/src:/usr/src/widget_app python:3 python /usr/src/widget_app/server.py
docker run -it --rm --name my-first-python-script -v $(pwd):/usr/src/widget_app python:3 python /usr/src/widget_app/server.py
# windows vers
docker run -it --rm --name my-first-python-script -v ${pwd}:/usr/src/widget_app python:3 python /usr/src/widget_app/server.py
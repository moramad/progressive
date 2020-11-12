## Docker Command

# build image from Docker file
docker build . --tag nama:versi

# run docker mongo bind mount port expose container
docker run -d --name mongo -p 27017:27017 -v "${pwd}/mongo/data/db:/data/db" -v "${pwd}/mongo/data/configdb:/data/configdb" mongo:latest
docker run -d --name mongo -p 27017:27017 -v mongo_db:/data/db  -v mongo_configdb:/data/configdb mongo:latest

# run docker python script
docker run -it --rm --name my-first-python-script -v /host_mnt/c/Users/mochamad/OneDrive/progressive/docker/docker-python/app/src:/usr/src/widget_app python:3 python /usr/src/widget_app/server.py
docker run -it --rm --name my-first-python-script -v $(pwd):/usr/src/widget_app python:3 python /usr/src/widget_app/server.py
# windows vers
docker run -it --rm --name my-first-python-script -v ${pwd}:/usr/src/widget_app python:3 python /usr/src/widget_app/server.py

# docker create volume influxdb
# docker run influxdb
# docker run -d --name influxdb -p 8086:8086 -v ${PWD}:/var/lib/influxdb influxdb
docker network create influxdb
docker run -d --name influxdb  -p 8086:8086 --net=influxdb -v influxdb:/var/lib/influxdb influxdb
docker run -d --name chronograf -p 8888:8888 --net=influxdb chronograf --influxdb-url=http://influxdb:8086 --influxdb-username=admin --influxdb-password
docker run -d --name=telegraf --net=influxdb telegraf

# GRAFANA
docker run -d -p 3000:3000 --name grafana grafana/grafana:latest

# ANSIBLE
docker run -it --rm --name ansible -v ${pwd}:/ansible centos-ansible:1.0 ansible-playbook /ansible/playbook.yml
docker run -it --rm --name ansible centos-ansible:1.0 /bin/sh

# Jenkins
docker run -d --name jenkins -v jenkins_home:/var/jenkins_home -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
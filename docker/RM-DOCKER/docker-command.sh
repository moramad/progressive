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
# docker run -d --name influxdb  -p 8086:8086 --net=influxdb -v influxdb:/var/lib/influxdb influxdb
# docker run -d --name influxdb  -p 8086:8086 --net=influxdb -v ${pwd}:/var/lib/influxdb influxdb
docker run -d --name influxdb  -p 8086:8086 --net=influxdb -v ${pwd}:/var/lib/influxdb -v ${pwd}/influxdb.conf:/etc/influxdb/influxdb.conf:ro influxdb
# docker run -d --name chronograf -p 8888:8888 --net=influxdb chronograf --influxdb-url=http://influxdb:8086
docker run -d --name chronograf -p 8888:8888 --net=influxdb chronograf --influxdb-url=http://influxdb:8086 --influxdb-username=admin --influxdb-password
# docker run --rm telegraf telegraf config > telegraf.conf # get config file
# docker run --rm telegraf telegraf -sample-config -input-filter file -output-filter influxdb > file.conf
docker run --rm --name=telegraf --net=influxdb -v ${pwd}:/etc/telegraf telegraf # run telegraf using volume and network
# docker run --rm kapacitor kapacitord config > kapacitor.conf
#docker run -d --name=kapacitor -h kapacitor -p 9092:9092 --net=influxdb -v ${pwd}/kapacitor.conf:/etc/kapacitor/kapacitor.conf:ro -e KAPACITOR_INFLUXDB_0_URLS_0=http://influxdb:8086 kapacitor
docker run --rm --name=kapacitor -p 9092:9092 --net=influxdb -v ${pwd}:/etc/kapacitor kapacitor
#docker run --rm -p 9092:9092 --name=kapacitor --net=container:influxdb kapacitor
# execute query command and send to file
# docker exec -ti influxdb sh -c "influx -database 'telegraf' -execute 'SELECT * FROM file' -format csv" > test.csv
# docker exec -ti influxdb sh -c "influx_inspect export -compress -out test -database telegraf" > test.csv
# COMMAND export data influxdb
influx_inspect export -database AHMITIOT -datadir /influx/var/lib/influxdb/data -waldir /influx/var/lib/influxdb/wal -out /root/.influxdb/export -start 2020-11-12T21:45:00+07:00
# COMMAND import data influxdb
docker exec -ti influxdb sh -c "influx -import -path=/var/lib/influxdb/export.txt"

# GRAFANA
docker run -d -p 3000:3000 --name grafana grafana/grafana:latest

# ANSIBLE
docker run -it --rm --name ansible -v ${pwd}:/ansible centos-ansible:1.0 ansible-playbook /ansible/playbook.yml
docker run -it --rm --name ansible centos-ansible:1.0 /bin/sh

# Jenkins
docker run -d --name jenkins -v ${pwd}/jenkins_home:/var/jenkins_home -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts


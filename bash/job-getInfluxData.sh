#!/bin/bash

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

printf "%s : " "Check Network Reachability"
PING=$(ping -w 3 -c 1 10.9.12.38 | grep received | awk -F" " '{print $4 }')    
if [[ $PING -eq "0"  ]]
then
    printf "[%s]\n" "${red}NOK${end}"
    exit 0
else
    printf "[%s]\n" "${grn}OK${end}"
fi

ONEDAY=$(date +%F)
ONEMINUTE=$(date +%X -d '1 minute ago')
ssh root@10.9.12.38 "influx_inspect export -database AHMITIOT -datadir /influx/var/lib/influxdb/data -waldir /influx/var/lib/influxdb/wal -out /root/.influxdb/export -start $(echo $ONEDAY)T$ONEMINUTE+07:00"
sftp root@10.9.12.38:/root/.influxdb/export export_$ONEDAY-$ONEMINUTE

mv export_$ONEDAY-$ONEMINUTE /mnt/d/Documents/PROGRESSIVE/docker/mount/influxdb/export_data
sudo docker exec -ti influxdb sh -c "influx -import -path=/var/lib/influxdb/export_data"

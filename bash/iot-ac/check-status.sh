#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

printf "%s : " "Check Network Reachability"
PING=$(ping -w 3 -c 1 172.24.24.1 | grep received | awk -F" " '{print $4 }')    
if [[ $PING -eq "0"  ]]
then
    printf "[%s]\n" "${red}NOK${end}"
    exit 0
else
    printf "[%s]\n" "${grn}OK${end}"
fi

cd /github/progressive/bash/iot-ac
INPUT=reference/LIST_INDOOR.lst
LOOKUP=reference/LOOKUP_AC_DESC.csv

HOST="10.9.12.35"
USERNAME="admin"
PASSWORD="ITIOT2019!"
TOPIC="sensor/#"
TOPIC="sensor"
INTERVAL="10"



NINPINGOK=0
NINPINGNOK=0
NOUTPINGOK=0
NOUTPINGNOK=0

[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

rm -rf logs/LIST_INDOOR_CONNECT logs/LIST_INDOOR_DISCONNECT logs/LIST_DATA_AC_ONGOING.csv logs/LIST_OUTDOOR_DISCONNECT

echo "================================"
echo "|             DESC             |"
echo "| $(date) |"
echo "================================"

echo "VASSETID,INDOOR,OUTDOOR,MQTT,CUR,VOL,HUM,TMP1,TMP2,TMP3,TMP4" >> logs/LIST_DATA_AC_ONGOING.csv

while read VIPADDRIN
do	    
    INDOOR="0"
    OUTDOOR="0"
    MQTT="0"
    CUR="0"
    VOL="0"
    HUM="0"
    TMP1="0"
    TMP2="0"
    TMP3="0"
    TMP4="0"

    VASSETID=$(awk -v VIPADDRIN="$VIPADDRIN" -F';' '{ if ($4 == VIPADDRIN) { print $1 } }' $LOOKUP)
    VDESC=$(awk -v VIPADDRIN="$VIPADDRIN" -F';' '{ if ($4 == VIPADDRIN) { print $2 } }' $LOOKUP)
    VCTRLID=$(awk -v VIPADDRIN="$VIPADDRIN" -F';' '{ if ($4 == VIPADDRIN) { print $3 } }' $LOOKUP)
    VIPADDROUT=$(awk -v VIPADDRIN="$VIPADDRIN" -F';' '{ if ($4 == VIPADDRIN) { print $5 } }' $LOOKUP)
    #echo "| $VASSETID | $VDESC | $VCTRLID | $VIPADDRIN | $VIPADDROUT |"    
    
    PING=$(ping -w $INTERVAL -c 1 $VIPADDRIN | grep received | awk -F" " '{print $4 }')    
    if [[ $PING -gt "0"  ]]
    then
        NINPINGOK=$((NINPINGOK+1))     

        echo $VIPADDRIN >> logs/LIST_INDOOR_CONNECT        
        INDOOR="1"
        
        if [ $VIPADDROUT == "indoor" ]
        then
            OUTDOOR="1"
        else
            PINGOUT=$(ping -w $INTERVAL -c 1 $VIPADDROUT | grep received | awk -F" " '{print $4 }')                     
            if [[ $PINGOUT -gt "0"  ]]
            then
                NOUTPINGOK=$((NOUTPINGOK+1))
                OUTDOOR="1"
            else
                NOUTPINGNOK=$((NOUTPINGNOK+1))
                echo $VIPADDROUT >> logs/LIST_OUTDOOR_DISCONNECT
            fi
        fi

        MQTT_RESULT=$(mosquitto_sub -h $HOST -u $USERNAME -P $PASSWORD -t $TOPIC/$VCTRLID -C 1 -W 5)
        if [ -z "$MQTT_RESULT" ]
        then            
            echo -e "$VASSETID | $VDESC | $VIPADDRIN | MQTT: [${RED}NOK${NC}]"
        else            
            MQTT="1"
            HUM=$(echo $MQTT_RESULT | jq '.SENSOR[0].NVALUE')
            TMP1=$(echo $MQTT_RESULT | jq '.SENSOR[1].NVALUE')
            TMP2=$(echo $MQTT_RESULT | jq '.SENSOR[2].NVALUE')
            TMP3=$(echo $MQTT_RESULT | jq '.SENSOR[3].NVALUE')
            TMP4=$(echo $MQTT_RESULT | jq '.SENSOR[4].NVALUE')
            VOL=$(echo $MQTT_RESULT | jq '.SENSOR[5].NVALUE')
            CUR=$(echo $MQTT_RESULT | jq '.SENSOR[6].NVALUE')            
        fi
        
    else        
        NINPINGNOK=$((NINPINGNOK+1)) 

        echo -e "$VASSETID | $VDESC | $VIPADDRIN | PING: [${RED}NOK${NC}]"
        echo $VIPADDRIN >> logs/LIST_INDOOR_DISCONNECT        
    fi                
    echo "$VASSETID,$INDOOR,$OUTDOOR,$MQTT,$CUR,$VOL,$HUM,$TMP1,$TMP2,$TMP3,$TMP4" >> logs/LIST_DATA_AC_ONGOING.csv
done < $INPUT
echo "==============================="
echo "TOTAL : $NINPINGOK Indoor Connected"
echo "TOTAL : $NOUTPINGOK Outdoor Connected"
echo "$(date)"
echo "==============================="

cp logs/LIST_DATA_AC_ONGOING.csv /DRIVE-C/Users/mochamad/OneDrive\ -\ PT\ Astra\ Honda\ Motor/Notebooks/SYNC2LINUX/LIST_DATA_AC.csv
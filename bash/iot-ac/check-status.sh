#!/bin/bash

INPUT=logs/LIST_INDOOR_CONNECT
LOOKUP=reference/LOOKUP_AC_DESC.csv
HOST="10.9.12.35"
USERNAME="admin"
PASSWORD="ITIOT2019!"
TOPIC="sensor/#"
TOPIC="sensor"
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

echo "==============================="
echo "|            DESC             |"
echo "==============================="

while read VIPADDRIN
do	    
    VASSETID=$(awk -v VIPADDRIN="$VIPADDRIN" -F',' '{ if ($4 == VIPADDRIN) { print $1 } }' $LOOKUP)
    VDESC=$(awk -v VIPADDRIN="$VIPADDRIN" -F',' '{ if ($4 == VIPADDRIN) { print $2 } }' $LOOKUP)
    VCTRLID=$(awk -v VIPADDRIN="$VIPADDRIN" -F',' '{ if ($4 == VIPADDRIN) { print $3 } }' $LOOKUP)
    VIPADDROUT=$(awk -v VIPADDRIN="$VIPADDRIN" -F',' '{ if ($4 == VIPADDRIN) { print $5 } }' $LOOKUP)
    
    echo "| $VASSETID | $VDESC | $VCTRLID | $VIPADDRIN | $VIPADDROUT |"    
    
    PING=$(ping -w 20 -c 1 $VIPADDRIN | grep received | awk -F" " '{print $4 }')
    if [[ $RESULT -gt "0"  ]]
    then
        echo "$IP: OK"
        echo $IP >> logs/LIST_INDOOR_CONNECT
        echo "$IP,OK" >> logs/LIST_INDOOR_RESULT
        RESULT=$(mosquitto_sub -h $HOST -u $USERNAME -P $PASSWORD -t $TOPIC/$VCTRLID -C 1 -W 5)
    else
            echo "$IP: NOK"
            echo $IP >> logs/LIST_INDOOR_DISCONNECT
            echo "$IP,NOK" >> logs/LIST_INDOOR_RESULT
    fi
        
    exit 0
done < $INPUT

echo "==============================="
NITEM=$(cat $INPUT | wc -l)
echo "TOTAL : $NITEM Connected"






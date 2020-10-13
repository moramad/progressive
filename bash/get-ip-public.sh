#!/bin/bash

IPPUB=$(curl ipinfo.io/ip)
if [[ $IPPUB == *"1"* ]]
then
	echo "$(date) | $IPPUB" >> /tmp/report-ip-public.lst
fi

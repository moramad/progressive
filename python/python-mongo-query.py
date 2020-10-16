#!/usr/bin/env python3

from pymongo import MongoClient

client = MongoClient("mongodb://192.168.100.6:27017/")
db = client["AHMITIOT"]
col = db["IOTAC"]

query = { "VASSETID" : { "$regex": "^ACO" } }

doc = col.find(query)

for x in doc:
    VASSETID = x['VASSETID']
    VDESC = x['VDESC']
    IPADDRIN = x['IPADDRIN']
    print ("{} | {} | {}".format(VASSETID,VDESC,IPADDRIN))
#!/usr/bin/env python3

from pymongo import MongoClient
client = MongoClient("mongodb://192.168.100.6:27017/")

with client:
    db = client.AHMITIOT

LISTAC = [ { 
    'VASSETID' : 'ACO.P1.H5.RMCIA.013',
    'VDESC' : 'AC GD H LT 5 R. CARISA',
    'IPADDRIN' : '172.24.24.21'
}]

DATAAC = {}
DATAAC['_id'] = VASSETID
DATAAC['VASSETID'] = VASSETID
DATAAC['INDOOR'] = INDOOR
DATAAC['OUTDOOR'] = OUTDOOR
DATAAC['DUPDATE'] = DUPDATE

db.IOTAC.insert_many(LISTAC)

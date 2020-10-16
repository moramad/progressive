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

db.IOTAC.insert_many(LISTAC)

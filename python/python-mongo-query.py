#!/usr/bin/env python3
from pymongo import MongoClient
import subprocess
from datetime import datetime
import json

client = MongoClient("mongodb://192.168.100.6:27017/")
DB = client["AHMITIOT"]
COLLECTION = DB["IOTAC"]
COLLECTION2 = DB["DATAAC"]

NINPINGOK=0
NINPINGNOK=0
NOUTPINGOK=0
NOUTPINGNOK=0
DUPDATE="01-01-2000 00:00:00"
DNOW=datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def is_reacheable(ip):
    if subprocess.call('ping -w3 -c1 ' + ip + '| grep received | awk -F" " \'{print $4 }\'', shell=True, stdout=subprocess.PIPE) == 0:
        return 1
    else:
        return 0

def select_document(query):
    try:
        result = COLLECTION.find(query)
        return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False

def update_document(query,set):
    try:
        COLLECTION.update(query,set)        
        return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False

def service_pinger(AC):
    global NINPINGOK
    global NINPINGNOK
    global NOUTPINGOK
    global NOUTPINGNOK

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

    VASSETID = AC['VASSETID']
    VDESC = AC['VDESC']
    VAREAIN = AC['VAREAIN']
    VAREAOUT = AC['VAREAOUT']
    VCTRLID = AC['VCTRLID']
    VIPADDRIN = AC['VIPADDRIN']
    VIPADDROUT = AC['VIPADDROUT']        
    
    PING_RESULT_IN = is_reacheable(VIPADDRIN)
                
    if PING_RESULT_IN == 1 :
        NINPINGOK+=1
        INDOOR = "1"
        DUPDATE = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if VIPADDROUT == "indoor" :
            OUTDOOR = "1"
        else:
            PING_RESULT_OUT = is_reacheable(VIPADDROUT)
            if PING_RESULT_OUT == 1 :
                NOUTPINGOK+=1
                OUTDOOR="1"
            else:
                NOUTPINGNOK+=1            
    else:
        NINPINGNOK+=1
        NOUTPINGNOK+=1
        print("{} | {} | {} | PING: NOK".format(VASSETID,VDESC,VIPADDRIN))                    
                        
    QUERY_SELECT_UPDATE = { "VASSETID": VASSETID }
    SET_VALUE_UPDATE = { "$set": { "INDOOR": INDOOR, "OUTDOOR": OUTDOOR, "DUPDATE": DUPDATE } } 
    # insert when ga ada, update when ada
    update_document(QUERY_SELECT_UPDATE, SET_VALUE_UPDATE)   

def main():    
    QUERY_SELECT_DATA = { "VASSETID" : { "$regex": "^SIM" } }
    QUERY_RESULT = select_document(QUERY_SELECT_DATA)
    
    for AC in QUERY_RESULT:       
        service_pinger(AC)                         

    print("===============================")
    print("TOTAL : {} Indoor Connected".format(NINPINGOK))
    print("TOTAL : {} Outdoor Connected".format(NOUTPINGOK))    
    print(DNOW)
    print("===============================")

if __name__ == '__main__':
    main()
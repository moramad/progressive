#!/usr/bin/env python3

###################################
# Feature Update : 
#   Cetak to csv result
#   Nyimpan Output to MongoDB
#   Get Data from mosquitto
###################################
from pymongo import MongoClient
from pymongo import errors
import subprocess
from datetime import datetime
import json
import sys
import threading

NINPINGOK=0
NINPINGNOK=0
NOUTPINGOK=0
NOUTPINGNOK=0
PING_INTERVAL="5"

def initialization_mongo():
    maxSevSelDelay = 1
    
    global COLLECTION
    try:
        client = MongoClient("mongodb://192.168.100.6:27017/",serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        DB = client["AHMITIOT"]
        COLLECTION = DB["IOTAC"]        

        return True
    except errors.ServerSelectionTimeoutError as err:    
        print(err)
        return False

def is_reacheable(ip):            
    if subprocess.call('ping -w' + PING_INTERVAL + ' -c1 ' + ip, shell=True, stdout=subprocess.PIPE) :
        return 0
    else:
        return 1

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
    DUPDATE = AC['DUPDATE']     
    
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
    update_document(QUERY_SELECT_UPDATE, SET_VALUE_UPDATE)   

def main():    
    print("===============================")
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("===============================")
    result = initialization_mongo()
    if result == True :
        # QUERY_SELECT_DATA = { "VASSETID" : { "$regex": "^ACO" } }
        QUERY_SELECT_DATA = {}
        QUERY_RESULT = select_document(QUERY_SELECT_DATA)
        
        threads = []
        for AC in QUERY_RESULT:  
            thr = threading.Thread(target=service_pinger, args=(AC,))
            thr.start()
            threads.append(thr)
        
        for thr in threads:
            thr.join()

        print("===============================")
        print("TOTAL : {} Indoor Connected".format(NINPINGOK))
        print("TOTAL : {} Outdoor Connected".format(NOUTPINGOK))    
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        print("===============================")
    else :
        sys.exit()    

if __name__ == '__main__':
    main()
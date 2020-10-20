#!/usr/bin/env python3

###################################
# Feature Update : 
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
import csv
from shutil import copyfile, Error

NINPINGOK=0
NINPINGNOK=0
NOUTPINGOK=0
NOUTPINGNOK=0
PING_INTERVAL="5"
ROWS = []
LIST_DATA_AC_PATH = 'logs/LIST_DATA_AC.csv'
LIST_DATA_AC_COMPLETE_PATH = '/DRIVE-C/Users/mochamad/OneDrive - PT Astra Honda Motor/Notebooks/SYNC2LINUX/LIST_DATA_AC.csv'

def initialization_mongo():
    maxSevSelDelay = 1
    
    global COLLECTION
    try:
        client = MongoClient("mongodb://192.168.0.100:27017/",serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        DB = client["DATAIOT"]
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

def csvwrite(path):
    global ROWS    
    FIELDS = ['DUPDATE','VASSETID','INDOOR','OUTDOOR','MQTT','CUR','VOL','HUM','TMP1','TMP2','TMP3','TMP4']

    try:
        with open(path,'w', newline='', encoding='utf-8') as csvfile:
            write = csv.writer(csvfile)
            write.writerow(FIELDS)
            for ROW in ROWS :
                write.writerow(ROW)
    except Exception as e:
        print("An Error occureed :: ", e)

def copy(src, dest):
    try:
        copyfile(src, dest)
    except Exception as e:
        print("An Error occureed :: ", e)

def service_pinger(AC):
    global ROWS
    global NINPINGOK
    global NINPINGNOK
    global NOUTPINGOK
    global NOUTPINGNOK

    ROWAC = []
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
    DUPDATE = AC['last']['DUPDATE']     
    
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
    SET_VALUE_UPDATE = { 
        "$set": { 
            "last" : {
                "DUPDATE": DUPDATE,
                "INDOOR": INDOOR, 
                "OUTDOOR": OUTDOOR,             
                'MQTT': MQTT,
                'CUR': CUR,
                'VOL': VOL,
                'HUM': HUM,
                'TMP1': TMP1,
                'TMP2': TMP2,
                'TMP3': TMP3,
                'TMP4': TMP4
            }
        } 
    }     
    update_document(QUERY_SELECT_UPDATE, SET_VALUE_UPDATE)
    ROWAC.extend((DUPDATE,VASSETID,INDOOR,OUTDOOR,MQTT,CUR,VOL,HUM,TMP1,TMP2,TMP3,TMP4))    
    ROWS.append(ROWAC)

def main():        
    print("===============================")
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("===============================")
    result = initialization_mongo()
    if result == True :
        QUERY_SELECT_DATA = { "VASSETID" : { "$regex": "^SIM" } }
        # QUERY_SELECT_DATA = {}
        QUERY_RESULT = select_document(QUERY_SELECT_DATA)
    
        threads = []
        for AC in QUERY_RESULT:              
            thr = threading.Thread(target=service_pinger, args=(AC,))
            thr.start()
            threads.append(thr)
        
        for thr in threads:
            thr.join()

        csvwrite(LIST_DATA_AC_PATH)
        copy(LIST_DATA_AC_PATH,LIST_DATA_AC_COMPLETE_PATH)

        print("===============================")
        print("TOTAL : {} Indoor Connected".format(NINPINGOK))
        print("TOTAL : {} Outdoor Connected".format(NOUTPINGOK))    
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        print("===============================")
    else :
        sys.exit()    

if __name__ == '__main__':
    main()
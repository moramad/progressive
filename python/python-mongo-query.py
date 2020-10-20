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

def initialization_mongo():
    maxSevSelDelay = 1
    
    global COLLECTION
    try:
        client = MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        DB = client["DATAIOT"]
        COLLECTION = DB["IOTAC"]        

        return True
    except errors.ServerSelectionTimeoutError as err:    
        print(err)
        return False

def select_document(query):
    try:
        result = COLLECTION.find(query)
        return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False

def main():    
    print("===============================")
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("===============================")
    result = initialization_mongo()
    if result == True :
        # QUERY_SELECT_DATA = { "VASSETID" : { "$regex": "^ACO" } }
        QUERY_SELECT_DATA = {}
        QUERY_RESULT = select_document(QUERY_SELECT_DATA)
        for AC in QUERY_RESULT :
            print(AC)

        print("===============================")       
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        print("===============================")
    else :
        sys.exit()    

if __name__ == '__main__':
    main()
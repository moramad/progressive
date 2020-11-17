
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from pymongo import MongoClient, errors
import subprocess
import platform
from datetime import datetime
import sys
import threading
import csv
from shutil import copyfile

LIST_AVGRUNHOUR_AC_PATH = 'logs/LIST_AVGRUNHOUR_AC.csv'
LIST_DAILYRUNHOUR_AC_PATH = 'logs/LIST_DAILYRUNHOUR_AC.csv'
LIST_LASTRUNHOUR_AC_PATH = 'logs/LIST_LASTRUNHOUR_AC.csv'
LIST_LASTMAINTENANCE_AC_PATH = 'logs/LIST_LASTMAINTENANCE_AC.csv'

ROW_AVGRUNHOUR = []
ROW_RUNHOURDAY = []
ROW_LASTRUNHOUR = []
ROW_LASTMAINTENANCE = []

SERIES = ""
COLLECTION = ""
COUNT = 0
OS = platform.system()

def initialization_influx():
    INFLUX_HOST = 'localhost'
    INFLUX_HOST = '10.9.12.38'    
    INFLUX_PORT = '8086'
    INFLUX_USERNAME = 'admin'
    INFLUX_PASSWORD = 'ITIOT2019!'
    INFLUX_DB = 'AHMITIOT'

    global SERIES
    try:
        if OS == 'Linux':
            # SERIES = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USERNAME,
            #                         INFLUX_PASSWORD)
            SERIES = InfluxDBClient(INFLUX_HOST, INFLUX_PORT)
        else:
            # windows kalau beda -->
            SERIES = InfluxDBClient(INFLUX_HOST, INFLUX_PORT)
            SERIES = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USERNAME,
                                    INFLUX_PASSWORD)
            
        SERIES.switch_database(INFLUX_DB)
        return True
    except Exception:
        print("Cannot connect influxDB!")
        return False


def select_series(query):
    try:
        RESULT = SERIES.query(query)
        return RESULT
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def initialization_mongo():
    maxSevSelDelay = 1
    global COLLECTION
    try:
        if OS == 'Linux':
            client = MongoClient("mongodb://192.168.56.1:27017/",
                                 serverSelectionTimeoutMS=maxSevSelDelay)
        else:
            client = MongoClient("mongodb://localhost:27017/",
                                 serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        DB = client["DATAIOT"]
        COLLECTION = DB["IOTAC"]
        return True
    except errors.ServerSelectionTimeoutError as err:
        print(err)
        return False


def select_document(query):
    try:
        RESULT = COLLECTION.find(query)
        return RESULT
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def update_document(query, set):
    try:
        COLLECTION.update_many(query, set)
        return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False

def write_csv(path, rows, fields):       
    try:
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            write = csv.writer(csvfile)
            write.writerow(fields)
            for ROW in rows:
                write.writerow(ROW)
    except Exception as e:
        print("An Error occureed :: ", e)

def service_maintenance(AC):
    global ROW_LASTMAINTENANCE
    ROWS_LASTMAINTENANCE = []    
    VASSETID = AC['VASSETID']
    QUERY = f''' SELECT NLSTHOUR, NLSTMTC, NVALUE, VASSETID, VPMID 
                 FROM "AHMITIOT_TXNEGPVASTS" WHERE VASSETID = \'{VASSETID}\''''
    results = select_series(QUERY) 

    NLSTHOUR = 0
    for measurement in results.get_points():        
        NLSTHOUR = measurement['NLSTHOUR']
        NLSTMTC = measurement['NLSTMTC']
        NVALUE = measurement['NVALUE']
        VPMID = measurement['VPMID']
                                        
        if NLSTHOUR is not None and NLSTMTC is not None:            
            ROWS_LASTMAINTENANCE.extend((VASSETID, NLSTHOUR, NLSTMTC, NVALUE, VPMID))
            ROW_LASTMAINTENANCE.append(ROWS_LASTMAINTENANCE)

def service_lastrunhour(AC):    
    global ROW_LASTRUNHOUR
    ROWS_LASTRUNHOUR = []

    VASSETID = AC['VASSETID']    

    QUERY = f'''SELECT last(NRUNHOUR) AS LASTRUNHOUR, VASSETID, time 
                FROM "AHMITIOT_TXNASSTACS"                
                WHERE VASSETID = \'{VASSETID}\' 
                AND time >= now() - 15m tz(\'Asia/Jakarta\')'''           
    results = select_series(QUERY) 

    LASTRUNHOUR = 0
    for measurement in results.get_points():        
        LASTRUNHOUR = measurement['LASTRUNHOUR']
        TIME = measurement['time']                                
        if LASTRUNHOUR is not None :            
            ROWS_LASTRUNHOUR.extend((TIME, VASSETID, LASTRUNHOUR))
            ROW_LASTRUNHOUR.append(ROWS_LASTRUNHOUR)
        # print (f"{VASSETID} | {LASTRUNHOUR:.2f}")        
    

def service_avgrunhour(AC):
    global COUNT
    global ROW_AVGRUNHOUR
    ROWS_AVGRUNHOUR = []

    VASSETID = AC['VASSETID']
    # VDESC = AC['VDESC']
    # VAREAIN = AC['VAREAIN']
    # VAREAOUT = AC['VAREAOUT']
    # VCTRLID = AC['VCTRLID']
    # VIPADDRIN = AC['VIPADDRIN']
    # VIPADDROUT = AC['VIPADDROUT']
    # DUPDATE = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    # DCONNECT = AC['last']['DCONNECT']    
    
    QUERY = f'''SELECT MEAN(DAILYRUNHOURS) AS NAVGRUNHOURDAY FROM 
                (SELECT (LAST(NRUNHOUR)-MIN(NRUNHOUR))/3600 AS DAILYRUNHOURS 
                FROM "AHMITIOT_TXNASSTACS" 
                WHERE VASSETID = \'{VASSETID}\' 
                AND time >= now() - 30w GROUP BY time(1d) 
                tz(\'Asia/Jakarta\')) WHERE DAILYRUNHOURS > 0'''           
    results = select_series(QUERY) 

    NAVGRUNHOURDAY=0
    for measurement in results.get_points():
        COUNT+=1        
        NAVGRUNHOURDAY = measurement['NAVGRUNHOURDAY']
        # TIME = measurement['time']                                
        if NAVGRUNHOURDAY is None :
            NAVGRUNHOURDAY = 0
        print (f"{VASSETID} | {NAVGRUNHOURDAY:.2f}")        
    ROWS_AVGRUNHOUR.extend((VASSETID, round(NAVGRUNHOURDAY,3)))
    ROW_AVGRUNHOUR.append(ROWS_AVGRUNHOUR)

def service_dailyrunhour(AC):    
    global ROW_RUNHOURDAY
    
    VASSETID = AC['VASSETID']    
    
    QUERY = f'''SELECT (LAST(NRUNHOUR)-MIN(NRUNHOUR))/3600 AS NRUNHOURDAY 
                FROM "AHMITIOT_TXNASSTACS" 
                WHERE VASSETID = \'{VASSETID}\' 
                AND time >= now() - 1w GROUP BY time(1d) tz(\'Asia/Jakarta\')'''           
    results = select_series(QUERY) 

    NRUNHOURDAY = 0
    TIME = "1970-01-01T00:00:00Z"
    for measurement in results.get_points():                      
        NRUNHOURDAY = measurement['NRUNHOURDAY']
        TIME = measurement['time']                                
        if NRUNHOURDAY is not None :                            
            ROWS_RUNHOURDAY = []
            ROWS_RUNHOURDAY.extend((TIME, VASSETID, round(NRUNHOURDAY,3)))
            ROW_RUNHOURDAY.append(ROWS_RUNHOURDAY)
        # print (f"{TIME} | {VASSETID} | {NRUNHOURDAY:.2f}")     

def main(): 
    global COUNT, ROW_AVGRUNHOUR, ROW_RUNHOURDAY, ROW_LASTRUNHOUR, ROW_LASTMAINTENANCE
    print("===============================")
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("===============================")

    CONNECT_INFLUX = initialization_influx()
    CONNECT_MONGO = initialization_mongo()
    if CONNECT_MONGO and CONNECT_INFLUX:
        QUERY_SELECT_DATA = {"VASSETID": {"$regex": "^ACO"}}
        QUERY_RESULT = select_document(QUERY_SELECT_DATA)
        COUNT = 0
        for AC in QUERY_RESULT:        
            service_avgrunhour(AC)
            service_dailyrunhour(AC)
            service_lastrunhour(AC)
            service_maintenance(AC)
        print (f"Total Data : {COUNT}")

        # Generate Report Daily Runhour AC
        ROW_RUNHOURDAY = sorted(ROW_RUNHOURDAY, key = lambda x:(x[1],x[0]))
        FIELDS = ['TIME','VASSETID', 'NRUNHOURDAY']        
        write_csv(LIST_DAILYRUNHOUR_AC_PATH,ROW_RUNHOURDAY,FIELDS)
                
        # Generate Report Average Runhour AC
        ROW_AVGRUNHOUR = sorted(ROW_AVGRUNHOUR, key = lambda x:x[1],reverse=True)
        FIELDS = ['VASSETID', 'NAVGRUNHOURDAY']        
        write_csv(LIST_AVGRUNHOUR_AC_PATH,ROW_AVGRUNHOUR,FIELDS)

        # Generate Report Last Runhour AC
        ROW_LASTRUNHOUR = sorted(ROW_LASTRUNHOUR, key = lambda x:(x[1],x[0]))
        FIELDS = ['TIME','VASSETID', 'LASTRUNHOUR']        
        write_csv(LIST_LASTRUNHOUR_AC_PATH,ROW_LASTRUNHOUR,FIELDS)

        # Generate Report Last Maintenance AC
        ROW_LASTMAINTENANCE = sorted(ROW_LASTMAINTENANCE, key = lambda x:(x[0]))
        FIELDS = ['VASSETID','NLSTHOUR','NLSTMTC','NVALUE','VPMID']
        write_csv(LIST_LASTMAINTENANCE_AC_PATH,ROW_LASTMAINTENANCE,FIELDS)
        

if __name__ == '__main__':
    main()

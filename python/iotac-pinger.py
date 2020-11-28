#!/usr/bin/env python3

###################################
# Feature Update:
#   Get Data from mosquitto
#   Set Historical Data
###################################
from influxdb import InfluxDBClient
from pymongo import MongoClient, errors
import subprocess
import platform
from datetime import datetime
import sys
import threading
import csv
from shutil import copyfile

NINPINGOK = 0
NINPINGNOK = 0
NOUTPINGOK = 0
NOUTPINGNOK = 0
COUNTNUM = 0
ROWS = []
SERIES = ""
COLLECTION = ""

PING_INTERVAL = "15"
LIST_DATA_AC_PATH = 'logs/LIST_DATA_AC.csv'
LIST_DATA_AC_COMPLETE_PATH = '/mnt/c/Users/mochamad/OneDrive - PT Astra Honda Motor/Notebooks/SYNC2LINUX/LIST_DATA_AC.csv'
OS = platform.system()


def initialization_influx():
    INFLUX_HOST = '10.9.12.38'
    INFLUX_PORT = '8086'
    INFLUX_USERNAME = 'admin'
    INFLUX_PASSWORD = 'ITIOT2019!'
    INFLUX_DB = 'AHMITIOT'

    global SERIES
    try:
        if OS == 'Linux':
            SERIES = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USERNAME,
                                    INFLUX_PASSWORD)
        else:
            # windows kalau beda -->
            SERIES = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USERNAME,
                                    INFLUX_PASSWORD)
        SERIES.switch_database(INFLUX_DB)
        return True
    except Exception:
        print("Cannot connect influxDB!")
        return False


def select_series(query, bind_params):
    try:
        RESULT = SERIES.query(query, bind_params=bind_params)
        return RESULT
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def initialization_mongo():
    maxSevSelDelay = 1
    global COLLECTION
    try:        
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


def write_csv(path):
    global ROWS
    FIELDS = ['DUPDATE', 'DCONNECT', 'VASSETID', 'INDOOR', 'OUTDOOR', 'MQTT',
              'CUR', 'VOL', 'HUM', 'TMP1', 'TMP2', 'TMP3', 'TMP4']

    try:
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            write = csv.writer(csvfile)
            write.writerow(FIELDS)
            for ROW in ROWS:
                write.writerow(ROW)
    except Exception as e:
        print("An Error occureed :: ", e)


def copy_file(src, dest):
    try:
        copyfile(src, dest)
    except Exception:
        # print("An Error occured :: ", e)
        print("Path : {} tidak ditemukan!".format(dest))


def is_reacheable(ip):
    if OS == 'Linux':
        if subprocess.call('ping -w ' + PING_INTERVAL + ' -c 1 ' + ip,
                           shell=True, stdout=subprocess.PIPE):
            return False
        else:
            return True
    else:
        if subprocess.call('ping -w ' + PING_INTERVAL*4000 + ' -n 1 ' + ip,
                           shell=True, stdout=subprocess.PIPE):
            return False
        else:
            return True


def service_pinger(AC):
    global ROWS
    global NINPINGOK
    global NINPINGNOK
    global NOUTPINGOK
    global NOUTPINGNOK
    global COUNTNUM

    ROWAC = []
    INDOOR = "0"
    OUTDOOR = "0"
    MQTT = "0"
    CUR = "0"
    VOL = "0"
    HUM = "0"
    TMP1 = "0"
    TMP2 = "0"
    TMP3 = "0"
    TMP4 = "0"

    VASSETID = AC['VASSETID']
    VDESC = AC['VDESC']
    # VAREAIN = AC['VAREAIN']
    # VAREAOUT = AC['VAREAOUT']
    # VCTRLID = AC['VCTRLID']
    VIPADDRIN = AC['VIPADDRIN']
    VIPADDROUT = AC['VIPADDROUT']
    DUPDATE = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    DCONNECT = AC['last']['DCONNECT']
    # DCONNECT = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    PING_RESULT_IN = is_reacheable(VIPADDRIN)
    if PING_RESULT_IN:
        NINPINGOK += 1
        INDOOR = "1"
        DCONNECT = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        COUNTNUM += 1
        # print("{} | {} | {} | {} | PING: OK".format(COUNTNUM, VASSETID, VDESC, VIPADDRIN))
        if VIPADDROUT == "indoor":
            OUTDOOR = "1"
        else:
            PING_RESULT_OUT = is_reacheable(VIPADDROUT)
            if PING_RESULT_OUT:
                NOUTPINGOK += 1
                OUTDOOR = "1"
            else:
                NOUTPINGNOK += 1
    else:
        NINPINGNOK += 1
        NOUTPINGNOK += 1
        COUNTNUM += 1
        print("{} | {} | {} | {} | PING: NOK".format(COUNTNUM, VASSETID, VDESC,
                                                     VIPADDRIN))
    bind_params = {'VASSETID': VASSETID}
    RESULT_INFLUX = select_series('''SELECT NRUNHOUR, DMODI FROM
                                  "AHMITIOT_DTLASSTACS" WHERE
                                  VASSETID=$VASSETID''', bind_params)
    for measurement in RESULT_INFLUX.get_points(
            measurement='AHMITIOT_DTLASSTACS'):
        NRUNHOUR = str(round(measurement['NRUNHOUR'] / 3600, 2))
        DMODI = measurement['DMODI']

    QUERY_SELECT_UPDATE = {"VASSETID": VASSETID}
    SET_VALUE_UPDATE = {
        "$set": {
            "last": {
                "DUPDATE": DUPDATE,
                "DCONNECT": DCONNECT,
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
            },
            "trend": {
                'NRUNHOUR': NRUNHOUR,
                'DMODI': DMODI
            }
        }
    }
    update_document(QUERY_SELECT_UPDATE, SET_VALUE_UPDATE)
    ROWAC.extend((DUPDATE, DCONNECT, VASSETID, INDOOR, OUTDOOR, MQTT,
                  CUR, VOL, HUM, TMP1, TMP2, TMP3, TMP4))
    ROWS.append(ROWAC)


def main():
    print("===============================")
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("===============================")
    CONNECT_IOT = is_reacheable('172.24.24.21')    
    CONNECT_INFLUX = initialization_influx()
    CONNECT_MONGO = initialization_mongo()
    if CONNECT_IOT and CONNECT_MONGO and CONNECT_INFLUX:
        # QUERY_SELECT_DATA = {"VASSETID": {"$regex": "^SIM"}}
        QUERY_SELECT_DATA = {"VASSETID": {"$regex": "^ACO"}}
        # QUERY_SELECT_DATA = {"VASSETID": {"$regex": "ACO.P1.A4.IT"}}
        QUERY_RESULT = select_document(QUERY_SELECT_DATA)
        threads = []
        for AC in QUERY_RESULT:
            thr = threading.Thread(target=service_pinger, args=(AC,))
            thr.start()
            threads.append(thr)
        for thr in threads:
            thr.join()
        write_csv(LIST_DATA_AC_PATH)
        copy_file(LIST_DATA_AC_PATH, LIST_DATA_AC_COMPLETE_PATH)
        print("===============================")
        print("TOTAL : {} Indoor Connected".format(NINPINGOK))
        print("TOTAL : {} Outdoor Connected".format(NOUTPINGOK))
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        print("===============================")
    else:
        if not CONNECT_IOT:
            print("Application Stopped. because cannot connect IoT Network")
        elif not CONNECT_MONGO:
            print("Application Stopped. because cannot connect MongoDB")
        elif not CONNECT_INFLUX:
            print("Application Stopped. because cannot connect InfluxDB")
        sys.exit()


if __name__ == '__main__':
    main()

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from pymongo import MongoClient, errors
import subprocess
import platform
from datetime import datetime
import json
import sys
import threading
import csv
from shutil import copyfile, Error
PING_INTERVAL = "1"

def is_reacheable(ip):            
    if OS == 'Linux' :
        if subprocess.call('ping -w ' + PING_INTERVAL + ' -c 1 ' + ip, shell=True, stdout=subprocess.PIPE) :
            return 0
        else:
            return 1
    else :
        if subprocess.call('ping -w ' + PING_INTERVAL*4000 + ' -n 1 ' + ip, shell=True, stdout=subprocess.PIPE) :
            return 0
        else:
            return 1

OS = platform.system()
CONNECT_IOT = is_reacheable('172.24.24.1') 
print(CONNECT_IOT)
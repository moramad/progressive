
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

HOST='t11317'
PORT='8086'
USERNAME='admin'
PASSWORD='ITIOT2019!'

def main(): 
    client = InfluxDBClient(HOST, PORT, USERNAME, PASSWORD)
    client.switch_database('AHMITIOT')
    # results = client.query('SELECT * FROM "AHMITIOT_DTLASSTACS"')  
    # results = client.query('SELECT (LAST(NRUNHOUR)-MIN(NRUNHOUR))/3600 AS DAILYRUNHOURS FROM "AHMITIOT_TXNASSTACS" WHERE VASSETID = \'ACO.P1.H1.GAEO1.016\'   AND time >= now() - 30d GROUP BY time(1d)')
    VASSETIDS = ["ACO.P1.A4.IT000.004","ACO.P1.H1.GAEO1.016"]   
    COUNT = 0     
    for VASSETID in VASSETIDS:
        QUERY = f'''SELECT MEAN(AVGPERDAY) AS AVGPERDAY FROM 
                (SELECT (LAST(NRUNHOUR)-MIN(NRUNHOUR))/3600 AS AVGPERDAY 
                FROM "AHMITIOT_TXNASSTACS" 
                WHERE VASSETID = \'{VASSETID}\' 
                AND time >= now() - 7d GROUP BY time(1d) 
                tz(\'Asia/Jakarta\')) WHERE AVGPERDAY > 0'''
        # print (QUERY)
        results = client.query(QUERY) 
            
        for measurement in results.get_points(measurement='AHMITIOT_TXNASSTACS'):
            COUNT+=1        
            AVGPERDAY = measurement['AVGPERDAY']
            TIME    = measurement['time']                                
            if AVGPERDAY is None :
                AVGPERDAY = 0
            print (f"{VASSETID} | {AVGPERDAY:.2f}".format(VASSETID,AVGPERDAY))
    print (f"Total Data : {COUNT}")
    write_csv(LIST_DATA_AC_PATH)

if __name__ == '__main__':
    main()

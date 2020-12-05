from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

HOST='t11317.astra-honda.com'
PORT='8086'
USERNAME='admin'
PASSWORD='ITIOT2019!'


def main(): 
    client = InfluxDBClient(HOST, PORT, USERNAME, PASSWORD)
    client.switch_database('AHMITIOT')
    results = client.query('SELECT * FROM "AHMITIOT_DTLASSTACS"')   
    COUNT = 0
    for measurement in results.get_points(measurement='AHMITIOT_DTLASSTACS'):
        COUNT+=1
        NRUNHOUR = measurement['NRUNHOUR'] 
        VASSETID = measurement['VASSETID']
        DMODI    = measurement['DMODI']        

        NRUNHOUR = NRUNHOUR/3600

        print ("{} | {:.2f} | {}".format(VASSETID,NRUNHOUR,DMODI))
    print ("Total Data : {}".format(COUNT))

if __name__ == '__main__':
    main()
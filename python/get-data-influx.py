
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

HOST='t11317'
PORT='8086'
USERNAME='admin'
PASSWORD='ITIOT2019!'


def main(): 
    client = InfluxDBClient(HOST, PORT, USERNAME, PASSWORD)
    client.switch_database('AHMITIOT')
    result = client.query('SELECT * FROM "AHMITIOT_DTLASSTACS"')
    print ("{0}".format(result))

if __name__ == '__main__':
    main()

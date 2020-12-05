import paho.mqtt.client as mqtt
import time

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
    
# The callback function for received message
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("rama")
# client.loop_forever()
client.loop_start()
print ("OK")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
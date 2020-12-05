import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.connect("test.mosquitto.org", 1883, 60)
for i in range(3):
    client.publish('rama', payload=i, qos=0, retain=False)
    print(f"send {i} to rama")
    time.sleep(1)
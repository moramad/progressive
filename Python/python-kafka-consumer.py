from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe(['my-topic'])
 
try :
    for message in consumer:    
        #get value from JSON
        data = message.value
        print(data['dataObjectID'])
        
except Exception:
    print (consumer)
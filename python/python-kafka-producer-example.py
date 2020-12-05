from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# bentuk struktur json
producer.send('my-topic', {"dataObjectID": "test1"})
producer.send('my-topic', {"dataObjectID": "test2"})
# bentuk struktur string
# producer.send('my-topic', b"test")

time.sleep(1)
# time.sleep(1)
producer.close()
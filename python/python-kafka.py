from confluent_kafka import Consumer

conf = {'bootstrap.servers': "host1:9092,
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
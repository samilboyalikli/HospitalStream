from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'hospital_kafka',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',      
    enable_auto_commit=True,           
    group_id='python-consumer-group',  
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Consumer started, waiting for messages...")

try:
    for message in consumer:
        print(f"Received message: {message.value}")
except KeyboardInterrupt:
    print("Consumer stopped manually.")
finally:
    consumer.close()
    print("Consumer finished.")

from kafka import KafkaConsumer
import json
import sys

consumer = KafkaConsumer(
    'children',                
    bootstrap_servers='kafka:9092',  
    auto_offset_reset='earliest',        
    enable_auto_commit=True,             
    group_id='python-consumer-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Consumer started, waiting for messages...")
message_counter = 0

try:
    for message in consumer:
        print(f"Received message: {message.value}")
        message_counter = message_counter + 1
        sys.stdout.flush()
        if message.value == "Distributor Stopped.":
            try: 
                consumer.close() 
                print("Closed")
            except Exception as e: 
                print(f"An error occured: {e}")
            print(f"There are {message_counter} children.")
            print("Consumer closed.")
except KeyboardInterrupt:
    print("Consumer stopped manually.")
    
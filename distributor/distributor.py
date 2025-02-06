from kafka import KafkaConsumer, KafkaProducer
import sys
import json

consumer = KafkaConsumer(
    'raw_stream',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='filter_group',
    value_deserializer=lambda x: x.decode('utf-8'),
    consumer_timeout_ms = 30000
)

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print(f"Listening to topic raw_stream...")

children_counter = 0
adult_counter = 0
senior_counter = 0

for message in consumer:
    try:
        data = json.loads(message.value)
        if data['Age'] < 18:
            print(f"Child: {message.value}")
            producer.send("children", data)
            children_counter = children_counter + 1
            sys.stdout.flush()
        elif data['Age'] >= 18 and data['Age'] < 65:
            print(f"Adult: {message.value}")
            producer.send("adult", data)
            adult_counter = adult_counter + 1
            sys.stdout.flush()
        elif data['Age'] >= 65:
            print(f"Senior: {message.value}")
            producer.send("senior", data)
            senior_counter = senior_counter + 1
            sys.stdout.flush()
    except KeyError:
        print(data)
        sys.stdout.flush()
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {message.value}")
        sys.stdout.flush()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.stdout.flush()

print(f"There are {children_counter} children.")
print(f"There are {adult_counter} adults.")
print(f"There are {senior_counter} seniors.")
stopper = {"status":"Distributor Stopped."}
topics = ["children", "adult", "senior"]

try:
    for topic in topics:
        producer.send(topic, stopper)
        producer.flush()
        print("Send message.")
except Exception as e:
    print(f"An error Occurred: {e}")

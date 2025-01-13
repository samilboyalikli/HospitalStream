from kafka import KafkaConsumer
import json

# Kafka Consumer'ı oluştur
consumer = KafkaConsumer(
    'hospital_kafka',                # Tüketilecek Kafka konusu
    bootstrap_servers='localhost:9092',  # Kafka broker adresi
    auto_offset_reset='earliest',        # İlk mesajdan başlamak için
    enable_auto_commit=True,             # Mesajları otomatik işaretle
    group_id='python-consumer-group',    # Consumer grubu tanımı
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # JSON veriyi çöz
)

print("Consumer started, waiting for messages...")

try:
    for message in consumer:
        # Mesaj verisini al ve işleyin
        print(f"Received message: {message.value}")
except KeyboardInterrupt:
    print("Consumer stopped manually.")
finally:
    consumer.close()
    print("Consumer finished.")

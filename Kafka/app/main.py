import sys

if len(sys.argv) > 1 and sys.argv[1] == "producer":
    import producer
else:
    import consumer

import os
import socket
import time

def wait_for_kafka(host: str, port: int, retries: int = 15, delay: int = 4):
    for i in range(retries):
        try:
            with socket.create_connection((host, port), timeout=3):
                print(f"✅ Kafka disponible en {host}:{port}")
                return True
        except OSError:
            print(f"⏳ Esperando a Kafka en {host}:{port}... ({i+1}/{retries})")
            time.sleep(delay)
    print("❌ Kafka no respondió a tiempo. Abortando.")
    exit(1)

# Leer host y puerto desde variable de entorno
kafka_address = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
kafka_host, kafka_port = kafka_address.split(":")
wait_for_kafka(kafka_host, int(kafka_port))

import time
import socket
import os

host, port = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092").split(":")
port = int(port)

for i in range(15):
    try:
        with socket.create_connection((host, port), timeout=3):
            print("Kafka está disponible.")
            break
    except OSError:
        print(f"Esperando a Kafka en {host}:{port}... ({i+1}/15)")
        time.sleep(4)
else:
    print("Kafka no respondió. Saliendo.")
    exit(1)

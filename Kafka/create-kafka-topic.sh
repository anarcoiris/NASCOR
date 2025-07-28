#!/bin/bash

# Nombre del topic
TOPIC_NAME="twitter-stream"

# Crear el topic
docker exec -it kafka kafka-topics \
  --create \
  --topic $TOPIC_NAME \
  --bootstrap-server kafka:9092 \
  --partitions 1 \
  --replication-factor 1

# Verificar si se creó correctamente
docker exec -it kafka kafka-topics \
  --list \
  --bootstrap-server kafka:9092
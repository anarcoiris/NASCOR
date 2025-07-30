import tweepy
from kafka import KafkaProducer
import json
import time
import os
import sys

# Variables externas
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
queries = os.getenv("SEARCH_QUERIES").split(",")
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INITIAL_DELAY = int(os.getenv("INITIAL_DELAY", 0))  # segundos
time.sleep(INITIAL_DELAY)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Twitter Client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets():
    for query in queries:
        print(f"Fetching tweets for query: {query}")
        tweets = client.search_recent_tweets(query=query, tweet_fields=["created_at", "text", "id"], max_results=10)
        if tweets.data:  # type: ignore
            for tweet in tweets.data:  # type: ignore
                tweet_data = {
                    "id": tweet.id,
                    "text": tweet.text,
                    "timestamp": str(tweet.created_at)
                }
                producer.send("twitter-stream", value=tweet_data)
                print(f"Tweet sent: {tweet_data}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "producer":
        print("🚦 Producer started")
        while True:
            try:
                fetch_tweets()
                time.sleep(60)  # intervalo normal
            except tweepy.TooManyRequests as e:
                print("⚠️  Límite de tasa alcanzado (429). Esperando 15 minutos...")
                time.sleep(15 * 60)  # espera obligatoria para Twitter
            except Exception as e:
                print(f"🛑 Error inesperado: {e}", file=sys.stderr)
                time.sleep(30)  # tiempo para errores generales
    else:
        import consumer  # Aquí importa el consumer si no es modo producer

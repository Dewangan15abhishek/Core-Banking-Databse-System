from kafka import KafkaProducer
import json

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers='localhost:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(f"Kafka not available: {e}")
            return None
    return _producer

def publish_transaction(txn_data: dict):
    producer = get_producer()
    if producer:
        producer.send('transactions', txn_data)
        producer.flush()
        print(f"Published to Kafka: {txn_data}")
    else:
        print(f"Kafka unavailable, skipping publish: {txn_data}")
from confluent_kafka import SerializingProducer
from config import KAFKA_BOOTSTRAP_SERVERS


class KafkaProducer:
    def __init__(self):
        self.producer = SerializingProducer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'error_cb': lambda err: print(f"Kafka Error: {err}")
        })

    def produce(self, topic, key, value, callback=None):
        """
        Asynchronously sends data to a Kafka topic.
        """
        self.producer.produce(
            topic,
            key=key,
            value=value,
            on_delivery=callback
        )
        # flush is optional here, but ensures immediate send
        self.producer.flush()

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

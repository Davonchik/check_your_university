from confluent_kafka import Producer, Consumer, KafkaException

class KafkaConsumer:
    def __init__(self, broker, topic, group_id="default_group"):
        self.broker = broker
        self.topic = topic
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.broker,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
            }
        )

    def consume_messages(self):
        self.consumer.subscribe([self.topic])
        print("Subscribed to topic. Waiting for messages...")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Error: {msg.error()}")
                else:
                    print(f"Received message: {msg.value().decode('utf-8')}")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    KAFKA_BROKER = "localhost:9092"
    TOPIC = "test"
    consumer = KafkaConsumer(KAFKA_BROKER, TOPIC, group_id="example_group")
    consumer.consume_messages()
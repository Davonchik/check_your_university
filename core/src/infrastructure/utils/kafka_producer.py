from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = Producer({"bootstrap.servers": self.broker})

    def delivery_report(self, err, msg):
        if err:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send_message(self, message):
        self.producer.produce(self.topic, message.encode("utf-8"), callback=self.delivery_report)
        self.producer.flush()
        print(f"Message '{message}' sent!")
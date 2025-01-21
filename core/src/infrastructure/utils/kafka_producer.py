from confluent_kafka import Producer
import threading

class KafkaProducer:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls, broker, topic):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(KafkaProducer, cls).__new__(cls)
                    cls._instance._initialise(broker, topic)
        return cls._instance

    def _initialise(self, broker, topic):
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
from confluent_kafka import Consumer
from aiogram import Bot
import asyncio


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
        loop = asyncio.get_event_loop()
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Error: {msg.error()}")
                else:
                    print(f"Received message: {msg.value().decode('utf-8')}")
                    message_content = msg.value().decode("utf-8")
                    loop.run_until_complete(self.send_notification(message_content))
        finally:
            self.consumer.close()
    def parse_message(self, message):
        
        return message.split(' ')
    async def send_notification(self, message):
        tg_id, status = self.parse_message(message)
        bot = Bot(token='7999109509:AAHWr1xadrAoA1IthlhNjnJzOMQ0XKho7Qo')
        chat_id = tg_id
        text = f"Request status: {status}"
        await bot.send_message(chat_id, text)

if __name__ == "__main__":
    KAFKA_BROKER = "kafka:9092"
    TOPIC = "test"
    consumer = KafkaConsumer(KAFKA_BROKER, TOPIC, group_id="example_group")
    consumer.consume_messages()
import pika
from datetime import timedelta

SESSIONS = []
KEYS = []
SOURCE = []

def get_chanel():
    parameters = pika.URLParameters("amqp://crawlers:rAt5HbgN9odP@192.168.5.46:5672/crawlers")
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    return channel


def update_time_timezone(my_time):
    return my_time + timedelta(hours=3)

def send_message(queue, body):
    try:
        channel = get_chanel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='',
                              routing_key=queue,
                              body=body)
    except Exception as e:
        print(f"send_message {e}")
        pass
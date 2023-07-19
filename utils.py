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


def challenge_code_handler(username, choice):
    from instagrapi.mixins.challenge import ChallengeChoice
    if choice == ChallengeChoice.SMS:
        return None
    elif choice == ChallengeChoice.EMAIL:
        return None
    return False


def get_settings(cl):
    settings = cl.get_settings()
    settings["authorization_data"] = cl.authorization_data
    settings["cookies"] = {
        "sessionid": cl.authorization_data["sessionid"]
    }
    return settings


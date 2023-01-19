import json
import time

import pika

from utils import get_chanel, SESSIONS

if __name__ == "__main__":
    channel = get_chanel()


    def callback(ch, method, properties, body):
        try:
            print(len(SESSIONS))
            while len(SESSIONS) > 10:
               time.sleep(2)
            SESSIONS.append(json.loads(body.decode("utf-8")))
        except Exception as e:
            print(f"callback{e}")

    channel.basic_consume(queue='insta_source_ig_session_new', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


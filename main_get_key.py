import json
import time

import pika

from utils import get_chanel, KEYS

if __name__ == "__main__":
    channel = get_chanel()

    def callback(ch, method, properties, body):
        try:
            print(len(KEYS))
            while len(KEYS) > 10:
               time.sleep(2)
            KEYS.append(json.loads(body.decode("utf-8")))
        except Exception as e:
            print(f"callback{e}")

    channel.basic_consume(queue='insta_source_parse_key', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


import json
import time

import pika

from utils import get_chanel, KEYS


def get_keys_while():
    while True:
        try:
            get_keys()
        except Exception:
            time.sleep(10)


def get_keys():
    channel = get_chanel()

    def callback(ch, method, properties, body):
        try:
            print(f"KEYS {len(KEYS)}")
            while len(KEYS) > 10:
                time.sleep(2)
            KEYS.append(json.loads(body.decode("utf-8")))
        except Exception as e:
            print(f"callback{e}")

    channel.basic_consume(queue='insta_source_parse_key', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    get_keys()

import json
import time

import pika

from utils import get_chanel, SOURCE


def get_source_while():
    while True:
        try:
            get_source()
        except Exception:
            time.sleep(10)


def get_source():
    channel = get_chanel()

    def callback(ch, method, properties, body):
        try:
            print(f"Source {len(SOURCE)}")

            while len(SOURCE) > 10:
                time.sleep(2)
            SOURCE.append(json.loads(body.decode("utf-8")))
        except Exception as e:
            print(f"callback{e}")

    channel.basic_consume(queue='insta_source_parse', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    get_source()

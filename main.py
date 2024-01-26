import threading
import time

from main_get_key import get_keys_while
from main_get_session import get_sessions_while
from main_get_source import get_source_while
from parse_key import parse_key
from parse_source import parse_source

session = None
amount = 30


def challenge_code_handler(username, choice):
    from instagrapi.mixins.challenge import ChallengeChoice
    if choice == ChallengeChoice.SMS:
        return None
    elif choice == ChallengeChoice.EMAIL:
        return None
    return False



if __name__ == '__main__':
    print("get_keys")
    i = 0
    x = threading.Thread(target=get_keys_while, args=())
    x.start()
    print("get_sessions")
    x = threading.Thread(target=get_sessions_while, args=())
    x.start()
    print("get_source")
    x = threading.Thread(target=get_source_while, args=())
    x.start()

    while True:
        print("start")
        try:
            session = parse_key(session)
        except Exception as e:
            print(f"parse_key: {e}")
        try:
            session = parse_source(session)
        except Exception as e:
            print(f"parse_source: {e}")
        # time.sleep(0)

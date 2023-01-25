import threading

from main_get_key import get_keys, get_keys_while
from main_get_session import get_sessions, get_sessions_while
from main_get_source import get_source, get_source_while
from parse_key import parse_key
from parse_source import parse_source

session = None
amount = 30
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
        try:
            parse_key(session)
        except Exception as e:
            print(f"parse_key: {e}")
        try:
            parse_source(session)
        except Exception as e:
            print(f"parse_source: {e}")

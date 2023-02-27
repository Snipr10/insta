import threading
import time
import multiprocessing

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
        print("start")
        try:
            # p = multiprocessing.Process(target=parse_key, name="parse_key", args=(None, ))
            # p.start()
            # n = 0
            # while n < 360:
            #     if p.is_alive():
            #         n += 1
            #     else:
            #         n = 360
            #     try:
            #         p.terminate()
            #     except Exception:
            #         pass
            #     try:
            #         p.join()
            #     except Exception:
            #         pass
            session = parse_key(session)
        except Exception as e:
            print(f"parse_key: {e}")
        try:
            session = parse_source(session)
            # p = multiprocessing.Process(target=parse_source, name="parse_source", args=(None,))
            # p.start()
            # n = 0
            # while n < 360:
            #     if p.is_alive():
            #         n += 1
            #     else:
            #         n = 360
            #     try:
            #         p.terminate()
            #     except Exception:
            #         pass
            #     try:
            #         p.join()
            #     except Exception:
            #         pass
        except Exception as e:
            print(f"parse_source: {e}")
        time.sleep(60)
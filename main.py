import threading
import time

from main_get_key import get_keys
from main_get_session import get_sessions
from utils import SESSIONS, KEYS, send_message, update_time_timezone
from instagrapi import Client
from django.utils import timezone

# Press the green button in the gutter to run the script.
session = None
amount = 30
if __name__ == '__main__':
    print("get_keys")
    i = 0
    x = threading.Thread(target=get_keys, args=())
    x.start()
    print("get_sessions")
    x = threading.Thread(target=get_sessions, args=())
    x.start()
    while True:
        try:
            i += 1
            print(i)
            banned = False
            if session is None and len(SESSIONS) == 0:
                time.sleep(10)
            else:
                if session is None:
                    session = SESSIONS.pop(0)
                key = KEYS.pop(0)
                try:
                    print("login")
                    cl = Client(
                        proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}")
                    cl.login(session["login"], session["password"])
                except Exception:
                    banned = True
                res = []
                is_parse_ok = True
                if not banned:
                    keyword = key["keyword"].replace(" ","")
                    try:
                        print("medias_top1")
                        medias_top1 = cl.hashtag_medias_top_v1(keyword, amount=amount)
                        res.extend(medias_top1)
                    except Exception as e:
                        is_parse_ok = False
                        pass
                    try:
                        print("medias_top2")
                        medias_top2 = cl.hashtag_medias_recent_v1(keyword, amount=amount)
                        res.extend(medias_top2)
                    except Exception as e:
                        is_parse_ok = False
                        pass

                    send_message("insta_source_parse_key_result", body={
                        "id": key.get("id"),
                        "last_modified": update_time_timezone(timezone.localtime()).isoformat()
                    })
                    send_message("insta_source_ig_session_parse", body={
                        "id": session.get("id"),
                        "last_parsing": update_time_timezone(timezone.localtime()).isoformat(),
                        "banned": banned
                    })
                    print(res)
                    send_message("insta_key_result", body=res)
                session = None
        except Exception as e:
            print(e)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

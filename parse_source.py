import datetime
import json
import time

from utils import SESSIONS, KEYS, send_message, SOURCE
from instagrapi import Client

amount = 30


def parse_source(session):
    try:
        print(f"sessions {len(SESSIONS)}   {session}")

        banned = False

        if session is None and len(SESSIONS) == 0:
            time.sleep(60)
        else:
            if session is None:
                session = SESSIONS.pop(0)
            if len(SESSIONS) == 0:
                time.sleep(60)
            else:
                source = SOURCE.pop(0)
                try:
                    print("login")
                    cl = Client(
                        proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}")
                    cl.login(session["login"], session["password"])
                except Exception as e:
                    print(f"login {e}")
                    banned = True
                res = []
                is_parse_ok = True
                if not banned:
                    try:
                        user_id = cl.user_id_from_username("sosedi_spch")
                        res = cl.user_medias(user_id, amount)
                    except Exception as e:
                        is_parse_ok = False
                        pass

                    print(res)

                    send_message("insta_source_parse_result", body=json.dumps({
                        "id": source["id"],
                        "last_modified": str(datetime.datetime.now())
                    }))
                    print("insta_key_result")
                    json_res = []
                    for r in res:
                        json_res.append(json.loads(r.json()))
                    send_message("insta_key_result", body=json.dumps(json_res))

                print("insta_source_ig_session_parse")
                send_message("insta_source_ig_session_parse", body=json.dumps({
                    "id": session["id"],
                    "last_parsing": str(datetime.datetime.now()),
                    "banned": banned
                }))
                session = None
    except Exception as e:
        print(f"While {e}")

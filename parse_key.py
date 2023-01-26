import datetime
import json
import time


from utils import SESSIONS, KEYS, send_message, SOURCE
from instagrapi import Client
amount = 30


def parse_key(session):
    try:
        # print(f"sessions {len(SESSIONS)}   {session}")

        banned = False

        if session is None and len(SESSIONS) == 0:
            pass
            # time.sleep(60)
        else:
            if session is None:
                session = SESSIONS.pop(0)
            if len(KEYS) == 0:
                print("No Keys")
                # time.sleep(60)
            else:
                key = KEYS.pop(0)
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
                    keyword = key["keyword"].replace(" ", "")
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
                    try:
                        for h in cl.search_hashtags(key["keyword"]):
                            medias_top1 = cl.hashtag_medias_top_v1(h.name, amount=amount)
                            res.extend(medias_top1)
                            medias_top2 = cl.hashtag_medias_recent_v1(h.name, amount=amount)
                            res.extend(medias_top2)
                    except Exception as e:
                        pass
                    print(res)

                    send_message("insta_source_parse_key_result", body=json.dumps({
                        "id": key["id"],
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
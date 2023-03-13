import datetime
import json
import time


from utils import SESSIONS, KEYS, send_message, SOURCE, challenge_code_handler
from instagrapi import Client
amount = 15


def parse_key(session):
    try:
        # print(f"sessions {len(SESSIONS)}   {session}")

        banned = False
        error_message = ""
        settings = None
        if session is None and len(SESSIONS) == 0:
            pass
            # time.sleep(60)
        else:
            if session is None:
                session = SESSIONS.pop(0)
            print(session)
            session_id = session['session_id']
            settings = session['settings']
            if len(KEYS) == 0:
                print("No Keys")
                # time.sleep(60)
            else:
                key = KEYS.pop(0)
                print(key)

                try:
                    if session['session_id'] is None:
                        raise Exception('session_id is None')

                    cl = Client(
                        proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}",
                        settings=session['settings']
                    )
                    cl.challenge_code_handler = challenge_code_handler
                    settings = cl.get_settings()
                    # cl.init()
                    # cl.login_by_sessionid(session['session_id'])
                    # session_id = session['session_id']
                    # print(f"Login Successfull {session_id}")
                except Exception as e:
                    banned = True
                    # error_message = str(e)
                    # session_id = None
                    # try:
                    #     print("login")
                    #     cl = Client(
                    #         proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}")
                    #     cl.challenge_code_handler = challenge_code_handler
                    #     cl.login(session["login"], session["password"])
                    #     session_id = cl.authorization_data['sessionid']
                    # except Exception as e:
                    #     error_message = str(e)
                    #     session_id = None
                    #     print(f"login {e}")
                    #     banned = True
                res = []
                is_parse_ok = True
                if not banned:
                    keyword = key["keyword"].replace(" ", "")
                    # try:
                    #     print("medias_top1")
                    #     medias_top1 = cl.hashtag_medias_top_v1(keyword, amount=amount)
                    #     res.extend(medias_top1)
                    # except Exception as e:
                    #     print(f"{e} {session_id}")
                    #     is_parse_ok = False
                    #     pass
                    # try:
                    #     print("medias_top2")
                    #     medias_top2 = cl.hashtag_medias_recent_v1(keyword, amount=amount)
                    #     res.extend(medias_top2)
                    # except Exception as e:
                    #     print(f"{e} {session_id}")
                    #     is_parse_ok = False
                    #     pass
                    try:
                        for h in cl.search_hashtags(key["keyword"]):
                            medias_top1 = cl.hashtag_medias_top_v1(h.name, amount=amount)
                            res.extend(medias_top1)
                            medias_top2 = cl.hashtag_medias_recent_v1(h.name, amount=amount)
                            res.extend(medias_top2)
                        settings = cl.get_settings()
                    except Exception as e:
                        error_message = str(e)
                        print(f"{e} {session_id}")
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
                    "banned": banned,
                    "error_message": error_message,
                    "session_id": session_id,
                    "settings": settings
                }))
            session = None
            settings = None
    except Exception as e:
        print(f"While {e}")
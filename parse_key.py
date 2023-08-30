import datetime
import json

from instagrapi.extractors import extract_media_v1

from utils import SESSIONS, KEYS, send_message, challenge_code_handler, get_settings, time_break
from instagrapi import Client

amount = 155


@time_break
def parse_key(session):
    try:
        # print(f"sessions {len(SESSIONS)}   {session}")

        banned = False
        error_message = ""
        settings = None
        if session is None and len(SESSIONS) == 0:
            raise Exception("no sessions")
            # time.sleep(60)
        else:
            if session is None:
                session = SESSIONS.pop(0)
            print(session)
            # session_id = session['session_id']
            settings = session['settings']

            errors = 0
            if len(KEYS) == 0:
                print("No Keys")
                # time.sleep(60)
            else:
                key = KEYS.pop(0)
                print(key)

                try:
                    # if session['session_id'] is None:
                    #     raise Exception('session_id is None')

                    cl = Client(
                        proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}",
                        settings=session['settings']
                    )
                    cl.challenge_code_handler = challenge_code_handler
                    settings = get_settings(cl)
                    # cl.init()
                    # cl.login_by_sessionid(session['session_id'])
                    # session_id = session['session_id']
                    # print(f"Login Successfull {session_id}")
                except Exception as e:
                    print(f"Client {key} {e}")
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
                        try:
                            next_max_id = None
                            medias_raw = []
                            try:
                                for i in range(amount):
                                    result = cl.private.get(
                                        'https://i.instagram.com/api/v1/fbsearch/search_engine_result_page/',
                                        params={'query': key["keyword"], 'next_max_id': next_max_id},
                                        proxies=cl.private.proxies
                                    ).json()
                                    next_max_id = result['reels_max_id']
                                    for s in result['sections']:
                                        # extract_media_v1(node["media"])
                                        try:
                                            layout_content = s['layout_content']
                                            try:
                                                medias_raw.extend(
                                                    list(layout_content['one_by_two_item']['clips']['items']))
                                            except Exception:
                                                pass
                                            try:
                                                medias_raw.extend(list(layout_content['fill_items']))
                                            except Exception:
                                                pass
                                            try:
                                                medias_raw.extend(list(layout_content['medias']))
                                            except Exception:
                                                pass
                                            print(1)
                                        except Exception:
                                            pass
                            except Exception as e:
                                errors += 1
                                print(f" {key} {e}")
                            for m in medias_raw:
                                try:
                                    res.append(extract_media_v1(m["media"]))
                                except Exception:
                                    pass
                            if next_max_id is None:
                                raise Exception("bad reuest")
                            settings = get_settings(cl)
                        except Exception:
                            errors += 1
                            for h in cl.search_hashtags(key["keyword"]):
                                medias_top1 = cl.hashtag_medias_top_v1(h.name, amount=amount)
                                res.extend(medias_top1)
                                medias_top2 = cl.hashtag_medias_recent_v1(h.name, amount=amount)
                                res.extend(medias_top2)
                            settings = get_settings(cl)
                    except Exception as e:
                        errors += 1
                        banned = True
                        error_message = str(e)
                        print(f"search_hashtags {key} {e}")
                        pass
                    print(key["keyword"])
                    print(res)
                    print(key.get("last_modified"))
                    if key.get("last_modified") is None:
                        key["last_modified"] = str(datetime.datetime.now())

                    print(
                        f'''{key["keyword"]}, {errors}, {banned}, {key["last_modified"] if errors > 1 or banned else str(datetime.datetime.now())} , now {datetime.datetime.now()}''')

                    send_message("insta_source_parse_key_result", body=json.dumps({
                        "id": key["id"],
                        "last_modified": key["last_modified"] if errors > 1 or banned else str(
                            datetime.datetime.now())
                    }))

                    json_res = []
                    for r in res:
                        json_res.append(json.loads(r.json()))
                    print(f"send {len(json_res)}")
                    send_message("insta_key_result", body=json.dumps(json_res))
                print("insta_source_ig_session_parse")

            send_message("insta_source_ig_session_parse", body=json.dumps({
                "id": session["id"],
                "last_parsing": str(datetime.datetime.now()),
                "banned": banned,
                "error_message": error_message,
                "session_id": None,
                "settings": settings
            }))
            session = None
            settings = None
    except Exception as e:
        print(f"While key {e}")

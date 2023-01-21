import threading

from main_get_key import get_keys
from main_get_session import get_sessions
from main_get_source import get_source
from parse_source import parse_source

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
    print("get_source")
    x = threading.Thread(target=get_source, args=())
    x.start()

    while True:
        # parse_key(session)
        parse_source(session)
    # while True:
    #     try:
    #         i += 1
    #         print(i)
    #         print(f"sessions {len(SESSIONS)}   {session}")
    #
    #         banned = False
    #
    #         if session is None and len(SESSIONS) == 0:
    #             time.sleep(60)
    #         else:
    #             if session is None:
    #                 session = SESSIONS.pop(0)
    #             if len(KEYS) == 0:
    #                 time.sleep(60)
    #             else:
    #                 source = SOURCE.pop(0)
    #                 try:
    #                     print("login")
    #                     cl = Client(
    #                         proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}")
    #                     cl.login(session["login"], session["password"])
    #                 except Exception as e:
    #                     print(f"login {e}")
    #                     banned = True
    #                 res = []
    #                 is_parse_ok = True
    #                 if not banned:
    #                     try:
    #                         user_id = cl.user_id_from_username("sosedi_spch")
    #                         res = cl.user_medias(user_id, 20)
    #                     except Exception as e:
    #                         is_parse_ok = False
    #                         pass
    #
    #                     print(res)
    #
    #                     send_message("insta_source_parse_result", body=json.dumps({
    #                         "id": source["id"],
    #                         "last_modified": str(datetime.datetime.now())
    #                     }))
    #                     print("insta_key_result")
    #                     json_res = []
    #                     for r in res:
    #                         json_res.append(json.loads(r.json()))
    #                     send_message("insta_key_result", body=json.dumps(json_res))
    #
    #
    #                 print("insta_source_ig_session_parse")
    #                 send_message("insta_source_ig_session_parse", body=json.dumps({
    #                     "id": session["id"],
    #                     "last_parsing": str(datetime.datetime.now()),
    #                     "banned": banned
    #                 }))
    #                 session = None
    #     except Exception as e:
    #         print(f"While {e}")

    # while True:
    #     try:
    #         i += 1
    #         print(i)
    #         print(f"sessions {len(SESSIONS)}   {session}")
    #
    #         banned = False
    #
    #         if session is None and len(SESSIONS) == 0:
    #             time.sleep(60)
    #         else:
    #             if session is None:
    #                 session = SESSIONS.pop(0)
    #             if len(KEYS) == 0:
    #                 time.sleep(60)
    #             else:
    #                 key = KEYS.pop(0)
    #                 try:
    #                     print("login")
    #                     cl = Client(
    #                         proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}")
    #                     cl.login(session["login"], session["password"])
    #                 except Exception as e:
    #                     print(f"login {e}")
    #                     banned = True
    #                 res = []
    #                 is_parse_ok = True
    #                 if not banned:
    #                     keyword = key["keyword"].replace(" ", "")
    #                     try:
    #                         print("medias_top1")
    #                         medias_top1 = cl.hashtag_medias_top_v1(keyword, amount=amount)
    #                         res.extend(medias_top1)
    #                     except Exception as e:
    #                         is_parse_ok = False
    #                         pass
    #                     try:
    #                         print("medias_top2")
    #                         medias_top2 = cl.hashtag_medias_recent_v1(keyword, amount=amount)
    #                         res.extend(medias_top2)
    #                     except Exception as e:
    #                         is_parse_ok = False
    #                         pass
    #                     print(res)
    #
    #                     send_message("insta_source_parse_key_result", body=json.dumps({
    #                         "id": key["id"],
    #                         "last_modified": str(datetime.datetime.now())
    #                     }))
    #                     print("insta_key_result")
    #                     json_res = []
    #                     for r in res:
    #                         json_res.append(json.loads(r.json()))
    #                     send_message("insta_key_result", body=json.dumps(json_res))
    #                 print("insta_source_ig_session_parse")
    #
    #                 send_message("insta_source_ig_session_parse", body=json.dumps({
    #                     "id": session["id"],
    #                     "last_parsing": str(datetime.datetime.now()),
    #                     "banned": banned
    #                 }))
    #                 session = None
    #     except Exception as e:
    #         print(f"While {e}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

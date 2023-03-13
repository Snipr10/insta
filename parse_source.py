import datetime
import json
import time

from utils import SESSIONS, KEYS, send_message, SOURCE, challenge_code_handler
from instagrapi import Client
from instagrapi.exceptions import UserNotFound

amount = 15


def parse_source(session):
    try:
        # print(f"sessions {len(SESSIONS)}   {session}")

        banned = False
        error_message = ""
        disabled = False
        is_parse_ok = True
        res = []
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

            if len(SESSIONS) == 0:
                print("No sessions")
                # time.sleep(60)
            else:
                source = SOURCE.pop(0)
                print(source)

                cl = Client(
                    proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}",
                    settings=session['settings']
                )
                settings = cl.get_settings()

                try:
                    user_id = cl.user_id_from_username(source["data"])
                    res = cl.user_medias(user_id, amount)
                    settings = cl.get_settings()

                except UserNotFound:
                    disabled = True
                except Exception as e:
                    is_parse_ok = False
                if not disabled and not is_parse_ok:
                    try:
                        print(f"session_id {session_id}")
                        if session['session_id'] is None:
                            raise Exception('session_id is None')
                        cl = Client(
                            proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}",
                            settings=session['settings']

                        )
                        cl.challenge_code_handler = challenge_code_handler
                        # cl.init()
                        # cl.login_by_sessionid(session['session_id'])
                        session_id = session['session_id']
                        settings = cl.get_settings()

                    except Exception as e:
                        error_message = str(e)
                        print(f"session id {e} {session_id}")
                        session_id = None
                        settings = None
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
                        try:
                            user_id = cl.user_id_from_username(source["data"])
                            res = cl.user_medias(user_id, amount)
                            settings = cl.get_settings()
                        except UserNotFound:
                            disabled = True
                        except Exception as e:
                            is_parse_ok = False
                            pass

            print(res)
            # if is_parse_ok:

            send_message("insta_source_parse_result", body=json.dumps({
                                "id": source["id"],
                                "last_modified": str(datetime.datetime.now()),
                                "disabled": disabled,

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
                "settings": settings,
            }))
            session = None
            settings = None
    except Exception as e:
        print(f"While {e}")
    return session

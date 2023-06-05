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
        disabled = 0
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

            # session_id = session['session_id']

            if len(SESSIONS) == 0:
                print("No sessions")
                raise Exception("No sessions")
                # time.sleep(60)
            else:
                source = SOURCE.pop(0)
                settings = session['settings']
                print(source)
                print(f"source date {source['last_modified']}")
                print(f"source date {datetime.datetime.fromisoformat(source['last_modified'])}")

                cl = Client(
                    proxy=f"http://{session['proxy_login']}:{session['proxy_pass']}@{session['proxy_ip']}:{session['proxy_port']}",
                    settings=session['settings']
                )
                settings = cl.get_settings()


                try:
                    print("start user")
                    user_id = cl.user_id_from_username(source["data"])
                except UserNotFound:
                    disabled = 1
                except Exception as e:
                    if "Status 404" in e:
                        disabled = 1
                    else:
                        print(f"user_id {e}")
                        is_parse_ok = False
                        banned = True

                if not banned and not disabled:
                    try:
                        print("start user")
                        res = cl.user_medias(user_id, amount)
                        settings = cl.get_settings()

                    except UserNotFound:
                        disabled = 1
                    except Exception as e:
                        if "Status 404" in e:
                            disabled = 1
                        else:
                            print(f"user_id {e}")
                            is_parse_ok = False
                            banned = True

            print(res)
            # if is_parse_ok:
            print(f"disabled {disabled}")
            send_message("insta_source_parse_result", body=json.dumps({
                                "id": source["id"],
                                "last_modified": source["last_modified"]  if banned or disabled else str(datetime.datetime.now()),
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
                "session_id": None,
                "settings": settings,
            }))
            session = None
            settings = None
    except Exception as e:
        print(f"While source {e}")
    return session

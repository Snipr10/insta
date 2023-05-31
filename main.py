import threading
import time

from instagrapi.extractors import extract_media_v1

from main_get_key import get_keys_while
from main_get_session import get_sessions_while
from main_get_source import get_source_while
from parse_key import parse_key
from parse_source import parse_source

session = None
amount = 30
from instagrapi import Client
def challenge_code_handler(username, choice):
    from instagrapi.mixins.challenge import ChallengeChoice
    if choice == ChallengeChoice.SMS:
        return None
    elif choice == ChallengeChoice.EMAIL:
        return None
    return False

if __name__ == '__main__':
    # f(1, 2, 3, x=4, y=5)
    # cl = Client(
    #     proxy=f"http://sega364_pd_gmail_com:5bd956afa2@176.53.166.175:30011",
    #     settings={'uuids': {'phone_id': '3ae9246b-a372-4b80-9932-8b348a522694', 'uuid': '7415c3c0-ddf0-47a8-8961-b55eb04ef744', 'client_session_id': 'bdcf31-8663-4b7a-ad24-d8999dd00ae3', 'advertising_id': '02d312df-e6c0-4c06-8989-8fb86a1fa7db', 'android_device_id': 'android-163b075c2c140cb7', 'request_id': 'aa844c4e-25b2-4e86-81ee-15969a6793ef', 'tray_session_id': '59ecc2e1-d355-4eff-b8e3-a1a5c97046f4'}, 'mid': 'ZHcXmQABAAFR_nUIvIqoX-PUOOZt', 'ig_u_rur': None, 'ig_www_claim': None, 'authorization_data': {'ds_user_id': '59494958372', 'sessionid': '59494958372%3Aj3Obwv9YI2Ndaa%3A24%3AAYcC3MnOmFF0xAgrDpze__zgK5MD8ONhYl35ROz6eQ'}, 'cookies': {'sessionid': '59494958372%3Aj3Obwv9YI2Ndaa%3A24%3AAYcC3MnOmFF0xAgrDpze__zgK5MD8ONhYl35ROz6eQ'}, 'last_login': None, 'device_settings': {'cpu': 'qcom', 'dpi': '80dpi', 'model': 'G011A', 'device': 'msm8998', 'resolution': '240x320', 'app_version': '25', 'manufacturer': 'google', 'version_code': '324500927', 'android_release': '7.1.2', 'android_version': '25'}, 'user_agent': 'Instagram 283.0.0.20.105 Android (25/7.1.2; 80dpi; 240x320; google; G011A; msm8998; qcom; en_US; 324500927)', 'country': 'US', 'country_code': 1, 'locale': 'en_US', 'timezone_offset': -14400}
    #
    # )
    # # self.private.get(
    # #     'https://i.instagram.com/api/v1/fbsearch/search_engine_result_page/',
    # #     params={'query': 'нуржан молдиярович', 'count': "100"}, proxies=self.private.proxies
    # # ).json()
    # # self.private.get(
    # #     'https://i.instagram.com/api/v1/fbsearch/search_engine_result_page/',
    # #     params={'query': 'нуржан молдиярович', 'next_max_id': 'r:e8b828d3b85d4d27b2fa53039d148b4e'},
    # #     proxies=self.private.proxies
    # # ).json()
    # next_max_id = None
    # medias_raw = []
    # try:
    #     for i in range(10):
    #         res = cl.private.get(
    #             'https://i.instagram.com/api/v1/fbsearch/search_engine_result_page/',
    #             params={'query': 'приложение', 'next_max_id': next_max_id},
    #             proxies=cl.private.proxies
    #         ).json()
    #         next_max_id = res['reels_max_id']
    #         for s in res['sections']:
    #             # extract_media_v1(node["media"])
    #             try:
    #                 layout_content = s['layout_content']
    #                 try:
    #                     medias_raw.extend(list(layout_content['one_by_two_item']['clips']['items']))
    #                 except Exception:
    #                     pass
    #                 try:
    #                     medias_raw.extend(list(layout_content['fill_items']))
    #                 except Exception:
    #                     pass
    #                 try:
    #                     medias_raw.extend(list(layout_content['medias']))
    #                 except Exception:
    #                     pass
    #                 print(1)
    #             except Exception:
    #                 pass
    # except Exception as e:
    #     print(e)
    # medias = []
    # for m in medias_raw:
    #     try:
    #         medias.append(extract_media_v1(m["media"]))
    #     except Exception:
    #         pass
    # cl.challenge_code_handler = challenge_code_handler
    # settings = cl.get_settings()
    # res = []
    # for h in cl.search_hashtags("auto"):
    #     medias_top1 = cl.hashtag_medias_top_v1(h.name, amount=amount)
    #     res.extend(medias_top1)
    #     medias_top2 = cl.hashtag_medias_recent_v1(h.name, amount=amount)
    #     res.extend(medias_top2)
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
        time.sleep(5)
import requests
from instance import *
from tenacity import *
import hashlib
import urllib.parse


def headers():
    return {
        'referer': 'https://www.bilibili.com',
        'Accept': 'application/json',
        'User-Agent': "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)",
    }


def headers_ffmpeg(video_url: str, video_title):
    user_agent = "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)"
    ffmpeg_headers = f'"User-Agent: {user_agent}" -headers "referer: https://www.bilibili.com"'
    return f'ffmpeg -user_agent {ffmpeg_headers} -i "{video_url}" -c copy "{video_title}" -loglevel quiet'


@retry(stop=stop_after_attempt(7), wait=wait_fixed(0.1))
def get(url: str, method="GET", params: dict = None):
    params = app_sign(params) if params else params
    if method == "GET":
        response = requests.request(url=url, method=method, headers=headers(), params=params)
    else:
        response = requests.request(url=url, method=method, headers=headers(), data=params)
    if response.status_code == 200:
        return response
    raise print("{}请求失败,code:".format(url, response.status_code))


def app_sign(params, appkey='1d8b6e7d45233436', appsec='560c52ccd288fed045859ed18bffd973'):
    """为请求参数进行 api 签名"""
    params.update({'appkey': appkey})
    params = dict(sorted(params.items()))  # 重排序参数 key
    query = urllib.parse.urlencode(params)  # 序列化参数
    params.update({'sign': hashlib.md5((query + appsec).encode()).hexdigest()})
    return params

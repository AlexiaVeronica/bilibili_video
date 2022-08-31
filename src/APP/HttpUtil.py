import requests
from instance import *
from tenacity import *


def headers():
    return {
        'referer': 'https://www.bilibili.com',
        'Accept': 'application/json',
        'User-Agent': "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)",
    }


def headers_ffmpeg():
    user_agent = "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)"
    return f'-user_agent "User-Agent: {user_agent}" -headers "referer: https://www.bilibili.com"'


def progress(data: [str], title: str, size: int, content_size: int):
    bar = '%s%.2f%%' % ("■" * int(size * 50 / content_size), float(size / content_size * 100))
    print('[下载进度]:', bar, end='\r')
    with open(f"{title}.flv", 'ab+') as file:  # 显示进度条
        file.write(data)


def download(url: str, title: str, params: dict = None):
    response = requests.get(url, headers=headers(), params=params, stream=True)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / 1024 / 1024))
    if response.status_code != 200:  # 判断是否响应成功 200为成功
        return response.status_code
    for index, data in enumerate(response.iter_content(chunk_size=1024)):
        size += len(data)
        progress(data, title, size, content_size)


@retry(stop=stop_after_attempt(7), wait=wait_fixed(0.1))
def get(url: str, method="GET", params: dict = None):
    if method == "GET":
        response = requests.request(url=url, method=method, headers=headers(), params=params)
    else:
        response = requests.request(url=url, method=method, headers=headers(), data=params)
    if response.status_code == 200:
        return response
    raise print("{}请求失败,code:".format(url, response.status_code))

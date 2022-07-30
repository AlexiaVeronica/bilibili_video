import requests
from fake_useragent import UserAgent
from rich import print

from instance import *


def headers():
    return {
        'referer': 'https://www.bilibili.com',
        'Accept': 'application/json',
        'User-Agent': "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)",
    }


def progress(data: [str], title: str, size: int, content_size: int):
    bar = '%s%.2f%%' % ("■" * int(size * 50 / content_size), float(size / content_size * 100))
    print('[下载进度]:', bar, end='\r')
    with open(f"{title}.flv", 'ab+') as file:  # 显示进度条
        file.write(data)


def download(url: str, title: str, params=None):
    response = requests.get(url, headers=headers(), params=params, stream=True)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / 1024 / 1024))
    if response.status_code != 200:  # 判断是否响应成功
        print(response.status_code)
        return response.status_code
    for index, data in enumerate(response.iter_content(chunk_size=1024)):
        size += len(data)
        progress(data, title, size, content_size)


def get(url: str, params=None, max_retry=10, *args, **kwargs):
    for retry in range(max_retry):
        result = requests.get(url=url, headers=headers(), params=params, *args, **kwargs)
        if result.status_code == 200:
            return result
        print("{}请求失败，第{}次重新请求：".format(url, retry))


def post(url, data=None, *args, **kwargs):
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        result = requests.post(url=url, headers=headers(), data=data, *args, **kwargs)
        if result.status_code == 200:
            return result
        print("{}请求失败，第{}次重新请求：".format(url, retry))


def put(url, data=None, *args, **kwargs):
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        result = requests.put(url=url, headers=headers(), data=data, *args, **kwargs)
        if result.status_code == 200:
            return result
        print("{}请求失败，第{}次重新请求：".format(url, retry))

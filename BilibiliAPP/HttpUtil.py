import requests
from fake_useragent import UserAgent
from rich import print


def headers():
    return {
        'referer': 'https://www.bilibili.com',
        'Accept': 'application/json',
        'User-Agent': "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)",
    }


def progress(s, c_s):
    print('[下载进度]:%s%.2f%%' %
          ('>' * int(s * 50 / c_s), float(s / c_s * 100)), end='\r')


def download(url: str, title: str,  max_retry=10, params=None):
    response = requests.get(url, headers=headers(), params=params, stream=True)
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    if response.status_code != 200:  # 判断是否响应成功
        return ""
    for index, data in enumerate(response.iter_content(chunk_size=1024)):
        progress(index, content_size)
        with open(f"{title}.flv", 'wb') as file:  # 显示进度条
            file.write(data)


def get(url: str, params=None, max_retry=10, *args, **kwargs):
    for retry in range(max_retry):
        result = requests.get(url=url, headers=headers(), params=params)
        if result.status_code == 200:
            return result
        print("{}请求失败，第{}次重新请求：".format(url, retry))


def post(url, data=None, *args, **kwargs):
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        result = requests.post(url=url, headers=headers(), data=data)
        if result.status_code == 200:
            return result
        print("{}请求失败，第{}次重新请求：".format(url, retry))


def put(url, data=None, *args, **kwargs):
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        result = requests.put(url=url, headers=headers(), data=data)
        if result.status_code == 200:
            return result
        print("{}请求失败，第{}次重新请求：".format(url, retry))

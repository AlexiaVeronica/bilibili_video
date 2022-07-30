import requests
import BilibiliAPP
from fake_useragent import UserAgent
from rich import print
import time



def download(url, params=None):
    start = time.time()  # 下载开始时间
    headers = {
        'referer': 'https://www.bilibili.com',
        'Accept': 'application/json',
        'User-Agent': "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)",
    }
    response = requests.get(url, headers=headers, params=params, stream=True)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    print(response.headers)
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    if response.status_code == 200:  # 判断是否响应成功
        print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / 1024 / 1024))  # 开始下载，显示下载文件大小
        with open("ssp.flv", 'wb') as file:  # 显示进度条
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                size += len(data)
                print('[下载进度]:%s%.2f%%' %
                      ('>' * int(size * 50 / content_size), float(size / content_size * 100)), end='\r')
    end = time.time()  # 下载结束时间
    print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间

if __name__ == '__main__':
    Transformation = BilibiliAPP.Transformation()
    print(Transformation.AV("BV11D4y1c7nP"))
    # print(enc(722602127))

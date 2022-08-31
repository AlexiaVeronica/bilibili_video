import requests
from instance import *

session = requests.Session()

headers = {
    'referer': 'https://www.bilibili.com',
    'Accept': 'application/json',
    'Keep-Alive': 'true',
    'User-Agent': "Mozilla/5.0 BiliDroid/6.37.1 (bbcallen@gmail.com)",
}


class Video:
    def __init__(self, video_info: dict):
        self.download_size = 0
        self.content_size = 0
        self.video_bv_id = video_info['bvid']
        self.video_aid = video_info['aid']
        self.video_pic = video_info['pic']
        self.video_title = video_info['title']
        self.video_tid = video_info['tid']
        self.video_cid = video_info['cid']
        self.video_desc = video_info['desc']

    def show_video_description(self):
        print('title:', self.video_title)
        print('bvid:', self.video_bv_id)
        print('aid:', self.video_aid)
        print('pic:', self.video_pic)
        print('tid:', self.video_tid)
        print('cid:', self.video_cid)
        print('desc:', self.video_desc)

    @property
    def save_path(self):
        return make_dirs(os.path.join("download", self.video_title))

    def add_progress(self):
        bar = '%s%.2f%%' % ("■" * int(self.download_size * 50 / self.content_size),
                            float(self.download_size / self.content_size * 100))
        print('[下载进度]:', bar, end='\r')

    def download(self, url: str, title: str, filesize: int, params: dict = None):
        self.content_size = filesize
        response = session.get(url, headers=headers, params=params, stream=True)
        print('Start download,[File size]:{size:.2f} MB'.format(size=self.content_size / 1024 / 1024))
        if response.status_code != 200:  # 判断是否响应成功 200为成功
            print('[请求失败]:', response.status_code)
            return response.status_code
        for data in response.iter_content(chunk_size=1024):
            self.download_size += len(data)
            self.add_progress()
            with open(os.path.join(self.save_path, f"{title}.flv"), 'ab+') as file:  # 显示进度条
                file.write(data)
        self.download_size = 0
        self.content_size = 0

import BilibiliAPP
import time
from rich import print


if __name__ == '__main__':
    video_url, title = BilibiliAPP.video_download_id("BV11D4y1c7nP")
    BilibiliAPP.HttpUtil.download(video_url, title)

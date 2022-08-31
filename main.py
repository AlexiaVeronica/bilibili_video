import argparse
import time
import re
from concurrent.futures import ThreadPoolExecutor

import src
import video
from instance import *
from rich import print


def shell_get_bilibili_video(bilili_bv: str):
    response = src.APP.View.web_interface_view(bilili_bv)
    if response.get("code") == 0:
        Vars.current_info = video.Video(response.get("data"))
        Vars.current_info.show_video_description()

    else:
        return print("get_bilibili_video:", response.get("message"))
    return True


def get_video_list(cid: str):
    response = src.APP.View.play_url_by_cid(bid=Vars.current_info.video_bv_id, cid=cid)
    for i in response['data']['durl']:
        Vars.current_page_list.append({"url": i['url'], "size": i['size']})


def shell_download_video():
    play_list = src.APP.View.get_play_list(Vars.current_info.video_bv_id)
    if len(play_list.get("data")) == 1:
        response = src.APP.View.play_url_by_cid(
            bid=Vars.current_info.video_bv_id, cid=Vars.current_info.video_cid
        )
        for i in response['data']['durl']:
            Vars.current_page_list.append({"url": i['url'], "size": i['size']})

    else:
        print("this video has multiple parts:{}\n".format(len(play_list.get("data"))))
        with ThreadPoolExecutor(max_workers=32) as executor:
            for play in play_list.get("data"):
                executor.submit(get_video_list, play['cid'])

    for index, i in enumerate(Vars.current_page_list):
        video_title = re.sub(r'[？?*|“<>:/]', '', Vars.current_info.video_title)
        Vars.current_info.download(url=i.get("url"), title=video_title, filesize=i.get("size"))
        # os.system(src.APP.HttpUtil.headers_ffmpeg(video_url, video_title + ".flv"))

    Vars.current_page_list.clear()


# 多线程下载
def start_parser():  # start parser for command line arguments and start download process
    parser = argparse.ArgumentParser()  # create parser object for command line arguments
    parser.add_argument(
        "-d", "--download",
        nargs=1, default=None, help="input image id to download it"
    )  # add download argument to parser object for command line arguments for download image
    parser.add_argument(
        "-c", "--cookies",
        nargs=1, default=None, help="input cookies to download it"
    )
    return parser.parse_args()


if __name__ == '__main__':
    argparse_args = start_parser()
    if argparse_args.download is not None:
        start = time.time()  # 下载开始时间 用于计算下载时间
        if shell_get_bilibili_video(bilili_bv=argparse_args.download[0]):
            shell_download_video()
            print('Download completed!, time: %.2f 秒' % (time.time() - start))  # output download time

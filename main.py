import argparse
import time
import re
import src
import video
from instance import *


def shell_get_bilibili_video(inputs_url: str):
    response = src.APP.View.web_interface_view(api_url=inputs_url)
    if response.get("code") == 0:
        Vars.video_current_info = video.Video(response.get("data"))
        Vars.video_current_info.show_video_description()
    else:
        return print("you input is not a valid bilibili video url")
    return True


def shell_download_video():
    response = src.APP.View.play_url_by_cid(
        qn="112", bid=Vars.video_current_info.video_bv_id, cid=Vars.video_current_info.video_cid
    )
    if response.get("code") == 0:
        video_url = [durl['url'] for durl in response.get("data")['durl']][0]
        video_title = re.sub(r'[？?*|“<>:/]', '', Vars.video_current_info.video_title)
        Vars.video_current_info.download(url=video_url, title=video_title)
        # os.system(src.APP.HttpUtil.headers_ffmpeg(video_url, video_title + ".flv"))
    else:
        print("download_video:", response.get("message"))


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
        if shell_get_bilibili_video(argparse_args.download[0]):
            shell_download_video()
            print('Download completed!, time: %.2f 秒' % (time.time() - start))  # output download time

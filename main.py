import argparse
import time
import re
import src
import video
from instance import *


def shell_download_video(inputs_url: str):
    start = time.time()  # 下载开始时间 用于计算下载时间
    Vars.video_info = src.BilibiliAPP.View.web_interface_view(api_url=inputs_url)
    if isinstance(Vars.video_info, dict) and Vars.video_info.get("code") == 0:
        Vars.video_info = video.Video(Vars.video_info.get("data"))
        Vars.video_info.show_video_description()
        response = src.BilibiliAPP.View.play_url_by_cid(
            qn="112", bid=Vars.video_info.video_bv_id, cid=Vars.video_info.video_cid
        )
        if response.get("code") == 0:
            video_url = [durl['url'] for durl in response.get("data")['durl']][0]
            video_title = re.sub(r'[？?*|“<>:/]', '', Vars.video_info.video_title)
            src.BilibiliAPP.HttpUtil.download(url=video_url, title=video_title)
        else:
            print("download_video:", response.get("message"))

        print('Download completed!, time: %.2f 秒' % (time.time() - start))  # output download time
    else:
        print("you input is not a valid bilibili video url")


def start_parser():  # start parser for command line arguments and start download process
    parser = argparse.ArgumentParser()  # create parser object for command line arguments
    parser.add_argument(
        "-d", "--download",
        nargs=1, default=None, help="input image id to download it"
    )  # add download argument to parser object for command line arguments for download image
    argparse_args = parser.parse_args()
    if argparse_args.download is not None:
        shell_download_video(argparse_args.download[0])


if __name__ == '__main__':
    start_parser()

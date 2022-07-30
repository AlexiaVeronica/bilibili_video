import argparse
import BilibiliAPP
from instance import *


def shell_download_video(inputs):
    start = time.time()  # 下载开始时间
    if len(inputs) >= 2:
        print("inputs:", inputs)
        video_url, title = BilibiliAPP.video_download_id(str(inputs))
        print(f"{title}, {video_url}")
        BilibiliAPP.HttpUtil.download(video_url, title)
        print('Download completed!,times: %.2f秒' % (time.time() - start))  # 输出下载用时时间
    else:
        print("没有输入bilibiliId")


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

import BilibiliAPP
from instance import *

def shell_downlaod_video(inputs):
    start = time.time()  # 下载开始时间
    if len(inputs) >= 2:
        video_url, title = BilibiliAPP.video_download_id(str(inputs[1]))
        BilibiliAPP.HttpUtil.download(video_url, title)
        print('Download completed!,times: %.2f秒' % (time.time() - start))  # 输出下载用时时间
    else:
        print("没有输入bilibiliId")


def shell():
    if len(sys.argv) > 1 and type(sys.argv) is list:
        command_line = True
        inputs = sys.argv[1:]
    else:
        command_line = False
        inputs = re.split('\\s+', input_('>').strip())
    while True:
        if inputs[0] == 'q' or inputs[0] == 'quit':
            sys.exit("已退出程序")
        elif inputs[0] == 'h' or inputs[0] == 'help':
            print("help")
        elif inputs[0] == 'd' or inputs[0] == 'download':
            shell_downlaod_video(inputs)
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', input_('>').strip())


if __name__ == '__main__':
    shell()

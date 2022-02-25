from BilibiliAPP import HttpUtil, UrlConstant
from rich import print
import re


def input_id(bilibili_id: str) -> dict:
    if re.findall(bilibili_id, "av") != -1:
        return UrlConstant.AID_INFO_API.format(
            Transformation().AV(re.sub(r"av", "", bilibili_id))
        )
    if re.findall(bilibili_id, "BV") != -1:
        return UrlConstant.AID_INFO_API.format(Transformation().AV(bilibili_id))


def video_download_id(bilibili_id: str):
    for index, retry in enumerate(range(10)):
        response = HttpUtil.get(input_id(bilibili_id)).json()
        if response.get("code") == 0:
            bv_id = response.get("data")['bvid']
            aid = response.get("data")['aid']
            title = response.get("data")['title']
            cid = response.get("data")['cid']
            return get_video_url(bv_id, cid, "112", title)
        else:
            print(f"retry：{index}\t", response.get("message"))


def get_video_url(bid, cid, qn, title) -> str:
    params = {
        'bvid': bid, 'qn': qn, 'cid': cid,
        'fnval': '0', 'fnver': '0', 'fourk': '1',
    }
    api_url = "https://api.bilibili.com/x/player/playurl"
    for index, retry in enumerate(range(10)):
        response = HttpUtil.get(api_url, params=params).json()
        if response.get("code") == 0:
            video_url = [durl['url'] for durl in response.get("data")['durl']]
            return video_url[0], title
        else:
            print(f"retry：{index}\t", response.get("message"))


class Transformation:
    def __init__(self):
        self.key = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        self.s = [11, 10, 3, 8, 4, 6]

    def AV(self, bv_id: str):
        tr = {}
        for i in range(58):
            tr[self.key[i]] = i
        r = 0
        for i in range(6):
            r += tr[bv_id[self.s[i]]] * 58 ** i
        return (r - 8728348608) ^ 177451812

    def BV(self, av_id: int):
        x = (av_id ^ 177451812) + 8728348608
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]] = self.key[x // 58 ** i % 58]
        return ''.join(r)

    # print(AV('BV17x411w7KC'))
    # print(BV(722602127))

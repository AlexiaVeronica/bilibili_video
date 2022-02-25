from BilibiliAPP import HttpUtil, UrlConstant
from rich import print
import re


def input_bili_id(bili_id: str) -> dict:
    bili_id = re.findall(r'video/(.*?)/?', bili_id)[0] if 'http' in bili_id else bili_id
    if re.findall(bili_id, "av") != -1:
        return UrlConstant.AID_INFO_API.format(
            Transformation().AV(re.sub(r"av", "", bili_id))
        )
    if re.findall(bili_id, "BV") != -1:
        return UrlConstant.AID_INFO_API.format(Transformation().AV(bili_id))


def video_download_id(bilibili_id: str, max_retry=10):
    for index, retry in enumerate(range(max_retry)):
        response = HttpUtil.get(input_bili_id(bilibili_id)).json()
        if response.get("code") == 0:
            bv_id = response.get("data")['bvid']
            aid = response.get("data")['aid']
            title = response.get("data")['title']
            cid = response.get("data")['cid']
            return get_video_url(bv_id, cid, "112", title)
        print(f"retry：{index}\t", response.get("message"))


def get_video_url(bid, cid, qn, title) -> str:
    for index, retry in enumerate(range(10)):
        params = {
            'bvid': bid, 'qn': qn, 'cid': cid,
            'fnval': '0', 'fnver': '0', 'fourk': '1',
        }
        response = HttpUtil.get(UrlConstant.VIDEO_API, params=params).json()
        if response.get("code") == 0:
            video_url = [durl['url'] for durl in response.get("data")['durl']]
            return video_url[0], title
        print(f"retry：{index}\t", response.get("message"))


class Transformation:
    @staticmethod
    def AV(bv_id: str):
        key = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        result = sum([{key[i]: i for i in range(58)}[bv_id[[11, 10, 3, 8, 4, 6][i]]] * 58 ** i for i in range(6)])
        return (result - 8728348608) ^ 177451812

    @staticmethod
    def BV(av_id: int):
        key = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        x = (av_id ^ 177451812) + 8728348608
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[[11, 10, 3, 8, 4, 6][i]] = key[x // 58 ** i % 58]
        return ''.join(r)

    # print(AV('BV17x411w7KC'))
    # print(BV(722602127))

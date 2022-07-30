import re
from src.APP import HttpUtil, UrlConstant
from instance import *


class View:
    @staticmethod
    def input_bili_id(bili_id: str) -> str:
        bili_id = re.findall("video/(\\w+)/?", bili_id)[0] if 'http' in bili_id else bili_id
        if bili_id.find('av') != -1 or bili_id.isdigit() is True:
            return UrlConstant.AID_INFO_API.format(re.sub(r"av", "", bili_id))
        elif bili_id.find("BV") != -1:
            return UrlConstant.AID_INFO_API.format(Transformation().AV(bili_id))

    @staticmethod
    def web_interface_view(api_url: str) -> dict:
        web_interface_view_url = View.input_bili_id(api_url)
        if web_interface_view_url != "":
            return HttpUtil.get(web_interface_view_url).json()

    @staticmethod
    def play_url_by_cid(bid: str, cid: str, qn: str) -> dict:  # get video play video url
        params = {'bvid': bid, 'qn': qn, 'cid': cid, 'fnval': '0', 'fnver': '0', 'fourk': '1'}
        return HttpUtil.get(UrlConstant.VIDEO_API, params=params).json()


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

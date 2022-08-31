import re
from src.APP import HttpUtil, UrlConstant


class View:

    @staticmethod
    def web_interface_view(bilili_bv: str) -> dict:
        return HttpUtil.get(UrlConstant.AID_INFO_API, params={"bvid": bilili_bv}).json()

    @staticmethod
    def get_play_list(bilili_bv: str):
        return HttpUtil.get(UrlConstant.APP_INFO_API, params={"bvid": bilili_bv}).json()

    @staticmethod
    def play_url_by_cid(bid: str, cid: str, qn: str = "112") -> dict:  # get video play video url
        params = {'bvid': bid, 'qn': qn, 'cid': cid, 'fnval': '0', 'fnver': '0', 'fourk': '1'}
        return HttpUtil.get(UrlConstant.VIDEO_API, params=params).json()

    # @staticmethod
    # def web_interface_view(api_url: str) -> dict:
    #     bili_id = re.findall("video/(\\w+)/?", api_url)[0] if 'http' in api_url else api_url
    #     if bili_id.find('av') != -1 or bili_id.isdigit() is True:
    #         return HttpUtil.get(UrlConstant.AID_INFO_API, params={"aid": re.sub(r"av", "", bili_id)}).json()
    #     elif bili_id.find("BV") != -1:
    #         return HttpUtil.get(UrlConstant.AID_INFO_API, params={"aid": Transformation.AV(bili_id)}).json()
    #     else:
    #         print("you input is not a valid bilibili video url")


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

# coding=utf-8
from config import *
from rich import print


class Vars:
    cfg = Config('Settings - Config.json', os.getcwd())


def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + len(left): pos2]
    return ''


def isCN(info):
    cn_no = 0
    for ch in str(info):
        if '\u4e00' <= ch <= '\u9fff':
            cn_no += 1
    return 20 - cn_no


def re_book_name(novel_name: str):
    return re.sub(r'[？?*|“<>:/]', '', novel_name)


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(
                    x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)


def write(path: str, mode: str, info=None):
    if info is not None:
        try:
            with open(path, f'{mode}', encoding='UTF-8', newline='') as file:
                file.writelines(info)
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(e)
            with open(path, f'{mode}', encoding='gbk', newline='') as file:
                file.writelines(info)
    else:
        try:
            return open(path, f'{mode}', encoding='UTF-8')
        except (UnicodeEncodeError, UnicodeDecodeError) as error:
            print(error)
            return open(path, f'{mode}', encoding='gbk')


def mkdir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def makedirs(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

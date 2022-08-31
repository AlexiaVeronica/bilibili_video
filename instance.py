# coding=utf-8 
from rich import print
import os
import json


class Config:
    file_path = None
    dir_path = None
    data = None

    def __init__(self, file_path, dir_path):
        self.file_path = file_path
        self.dir_path = dir_path
        self.data = {}

    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f) or {}
        except FileNotFoundError:
            try:
                if not os.path.isdir(self.dir_path):
                    os.makedirs(self.dir_path)
                with open(self.file_path, 'w'):
                    pass
            except Exception as e:
                print('error: ', e)
                print('error: while creating config file: ' + self.file_path)
        except Exception as e:
            print('error: ', e)
            print('error: while reading config file: ' + self.file_path)

    def save(self):
        try:
            if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print('error: ', e)
            print('error: while saving config file: ' + self.file_path)


class Vars:
    cfg = Config('Settings - Config.json', os.getcwd())
    current_info = None
    current_page_list = []

def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + len(left): pos2]
    return ''


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def mkdir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def make_dirs(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

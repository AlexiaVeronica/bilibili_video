import os
import json
import requests
import math

headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
     'Host': 'api.bilibili.com',
     'Cookie': ''
   }

def getAid(BVid):
    url = "http://api.bilibili.com/x/web-interface/view?bvid="+str(BVid)
    response = requests.get(url, headers=headers).json()
    AVID = response['data']['aid']
    return AVID


def getReplyPageNum(oid):
    url = "https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=1" + \
        "&type=1&oid="+str(oid)+"&sort=2"
    respond = requests.get(url, headers=headers).json()
    replyNum = int(respond['data']['page']['acount'])
    replyPageCount = int(respond['data']['page']['count'])
    replyPageSize = int(respond['data']['page']['size'])
    replyPageNum = math.ceil(replyPageCount/replyPageSize)
    # 返回评论的页数replyPageNum
    return replyPageNum


def pinglun(number, avid):
    url = f'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn={number}&type=1&oid={avid}&sort=2'
    respond = requests.get(url, headers=headers).json()
    for data in respond['data']['replies']:
        data = data['member']
        mid = data['mid']  # uid
        uname = data['uname'] # 名字
        sex = data['sex']  # 性别
        sign = data['sign']  # 个人简介
        avatar = data['uname'] # 头像
        for k, y in data.items():
            print(k, '--->',  y)


deta = """{'rpid': 5433549997,
	'oid': 250579623,
	'type': 1,
	'mid': 357221321,
	'root': 0,
	'parent': 0,
	'dialog': 0,
	'count': 0,
	'rcount': 0,
	'state': 0,
	'fansgrade': 1,
	'attr': 0,
	'ctime': 1632139797,
	'rpid_str': '5433549997',
	'root_str': '0',
	'parent_str': '0',
	'like': 0,
	'action': 0,
	'member': {
		'mid': '357221321',
		'uname': 'Leon_X_',
		'sex': '男',
		'sign': 'GGGGGGGGGGGGGGGGGGGFUNK',
		'avatar': 'http://i0.hdslb.com/bfs/face/52d178af4428d382ccfc03f6bda59fc4b017b6a2.jpg',
		'rank': '10000',
		'DisplayRank': '0',
		'level_info': {
			'current_level': 4,
			'current_min': 0,
			'current_exp': 0,
			'next_exp': 0
		},
		'pendant': {
			'pid': 0,
			'name': '',
			'image': '',
			'expire': 0,
			'image_enhance': '',
			'image_enhance_frame': ''
		},
		'nameplate': {
			'nid': 0,
			'name': '',
			'image': '',
			'image_small': '',
			'level': '',
			'condition': ''
		},
		'official_verify': {
			'type': -1,
			'desc': ''
		},
		'vip': {
			'vipType': 0,
			'vipDueDate': 0,
			'dueRemark': '',
			'accessStatus': 0,
			'vipStatus': 0,
			'vipStatusWarn': '',
			'themeType': 0,
			'label': {
				'path': '',
				'text': '',
				'label_theme': '',
				'text_color': '',
				'bg_style': 0,
				'bg_color': '',
				'border_color': ''
			},
			'avatar_subscript': 0,
			'nickname_color': ''
		},
		'fans_detail': {
			'uid': 357221321,
			'medal_id': 229056,
			'medal_name': 'LOOSE',
			'score': 0,
			'level': 3,
			'intimacy': 0,
			'master_status': 1,
			'is_receive': 1,
			'medal_color': 643602062,
			'medal_color_end': 643602062,
			'medal_color_border': 4284257934,
			'medal_color_name': 4284257934,
			'medal_color_level': 4284257934,
			'guard_level': 0
		},
		'following': 0,
		'is_followed': 0,
		'user_sailing': {
			'pendant': None,
			'cardbg': None,
			'cardbg_with_focus': None
		},
		'is_contractor': False
	},
	'content': {
		'message': '乌鸦哥发福了？',
		'plat': 0,
		'device': '',
		'members': [],
		'jump_url': {},
		'max_line': 6
	},
	'replies': [],
	'assist': 0,
	'folder': {
		'has_folded': False,
		'is_folded': False,
		'rule': 'https://www.bilibili.com/blackboard/foldingreply.html'
	},
	'up_action': {
		'like': False,
		'reply': False
	},
	'show_follow': False,
	'invisible': False,
	'reply_control': {}
}"""




if __name__ == '__main__':
    BV_number = input('输入BV号，注意不用加上BV\n')
    avid = getAid(BV_number)
    number = getReplyPageNum(avid)
    pinglun(str(number), str(avid))



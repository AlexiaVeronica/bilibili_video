class Video:
    def __init__(self, video_info: dict):
        self.video_bv_id = video_info['bvid']
        self.video_aid = video_info['aid']
        self.video_pic = video_info['pic']
        self.video_title = video_info['title']
        self.video_tid = video_info['tid']
        self.video_cid = video_info['cid']
        self.video_desc = video_info['desc']

    def show_video_description(self):
        print('title:', self.video_title)
        print('bvid:', self.video_bv_id)
        print('aid:', self.video_aid)
        print('pic:', self.video_pic)
        print('tid:', self.video_tid)
        print('cid:', self.video_cid)
        print('desc:', self.video_desc)

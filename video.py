class Video:
    def __init__(self, video_info: dict):
        self.video_bv_id = video_info['bvid']
        self.video_aid = video_info['aid']
        self.video_pic = video_info['pic']
        self.video_title = video_info['title']
        self.video_tid = video_info['tid']
        self.video_cid = video_info['cid']
        self.video_desc = video_info['desc']

import os
import time
from celery import task
from utils.base_qiniu import Qiniu
from client.models import VideoSub

@task
def video_task(path_name, video_file_name, video_sub_id):
    # 上传视频到七牛云
    if not os.path.exists(path_name):
        return False
    final_name = '{}_{}'.format(int(time.time()), video_file_name)
    url = Qiniu.put(final_name, path_name)

    # 如果上传成功则保存到数据库
    if url:
        try:
            video_sub = VideoSub.objects.get(video_sub_id)
            video_sub.url = 'http://' + url
            video_sub.save()
            return True
        except:
            return False
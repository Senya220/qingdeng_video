import os
import shutil
import time
from django.conf import settings
from client.models import Video, VideoSub
from tasks.task import video_task
def chekcAndGetVideoType(type_obj, type_value, message):
    """

    :param type_obj: type对象(用户传的对象)
    :param type_value: 数据库中存储的视频类型
    :param message:
    :return:
    """
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}
    return {'code': 0, 'msg': 'success'}

def handle_video(video_file, video_id, number):
    """
    拷贝本地文件到temp_in
    :param video_file:
    :param video_id:
    :param number:
    :return:
    """
    #本地文件拷贝到temp_in
    in_path = os.path.join(settings.BASE_DIR,'temp_in')
    name = "{}_{}".format(time.time(),video_file.name)
    path_name = '/'.join(in_path, name)
    temp_path = video_file.temporary_file_path()
    #
    shutil.copyfile(temp_path, path_name)

    video = Video.objects.get(pk=video_id)

    video_sub = Video.objects.create(
        video=video,
        number=number,
        # url需要等待用户上传成功后才能返回  最耗时
        # url='http://' + url,
        url='',
    )
    video_task.delay(path_name, video_file.name, video_sub.id)
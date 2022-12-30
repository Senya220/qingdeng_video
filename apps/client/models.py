import datetime
from enum import Enum
from django.db import models


# Create your models here.
class VideoType(Enum):
    meiti = 'meiti'
    other = 'other'

VideoType.meiti.label = 'meiti'
VideoType.other.label = 'other'

class FromType(Enum):
    youku = 'youku'
    custom = 'custom'

FromType.youku.label = '优酷'
FromType.custom.label = '自制'

class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'

NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国'
NationalityType.other.label = '其他'

class IdentityType(Enum):
    to_star = 'to_star'
    supporting_rule = 'supporting_rule'
    director = 'director'


IdentityType.to_star.label = '主演'
IdentityType.supporting_rule.label = '配角'
IdentityType.director.label = '导演'



class Video(models.Model):
    """
    不知道是那个类  定义的字段有那些，先写个假的
    """
    # 视频名称
    name = models.CharField(max_length=100, null=False)
    # 海报
    image = models.CharField(max_length=500, default='')
    # 视频类型
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    # 视频来源
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    # 视频地区来源
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    # 视频简介
    info = models.TextField()
    #
    status = models.BooleanField(default=True, db_index=True)
    # 视频创建时间
    create_time = models.DateTimeField(auto_now=True)
    # 视频修改时间
    modify_time = models.DateTimeField(auto_now=True)
    # 操作：编辑 | 附属信息
    operate = models.CharField(max_length=100, null=False)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return '电影名称：{}'.format(self.name)


class VideoStar(models.Model):
    video = models.ForeignKey(Video, related_name='video_star', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    # 演员身份[例如：主演]
    identity = models.CharField(max_length=50, default=IdentityType.to_star.value)

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return '演员名称：{}'.format(self.name)


class VideoSub(models.Model):
    video = models.ForeignKey(Video, related_name='video_stub', on_delete=models.SET_NULL, blank=True, null=True)
    url = models.CharField(max_length=500, null=False)

    # 电影集数
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'url', 'number')

    def __str__(self):
        return '电影名称：{}, 电影集数：{}'.format(self.video.name, self.number)

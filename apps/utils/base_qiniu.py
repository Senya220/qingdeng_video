from qiniu import Auth, put_data, put_file
from django.conf import settings

class Qiniu:
    def __init__(self,bucket_name, base_url):
        self.bucket_name = bucket_name
        self.base_url = base_url
        self.qiniu = Auth(settings.QINIU_AK, settings.QINIU_SK)

    #上传方法
    def put(self, name, path):
        token = self.qiniu.upload_token(self.bucket_name, name)
        ret, info = put_file(token, name, path)

        if 'key' in ret:
            remote_url = '/'.join([self.base_url, ret['key']])
            return remote_url

video_url = Qiniu(bucket_name=settings.QINIU_VIDEO, base_url=settings.QINIU_VIDEO_URL)
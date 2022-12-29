from django.shortcuts import redirect, reverse
from django.views.generic import View
from libs.base_rander import render_to_resoponse
from django.contrib.auth import authenticate
from .models import Video, VideoStub, VideoStar, VideoType, FromType, NationalityType, IdentityType
from utils.common import chekcAndGetVideoType

# Create your views here.
# 外链视频视图
class ExternalVideo(View):
    def get(self, request):
        error = request.GET.get('error', '')
        data = {'error': error}
        # 查找用户自制视频之外的所有视频
        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos
        if authenticate(request.user):
            return render_to_resoponse(request, 'dashboard/video/external_video.html')
        return redirect(reverse('dashboard_login'))

    def post(self, request):
        name = request.POST.get('name', '')
        image = request.POST.get('image', '')
        video_type = request.POST.get('video_type', '')
        from_to = request.POST.get('from_to', '')
        nationality = request.POST.get('nationaltity', '')
        info = request.POST.get('info', '')

        # 必填字段判断
        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(reverse('external_video'), '缺少必要信息'))

        #视频验证
        result = chekcAndGetVideoType(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))

        # 视频来源
        result = chekcAndGetVideoType(FromType, from_to, '非法来源')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))

        #非法地区
        result = chekcAndGetVideoType(NationalityType, nationality, '非法地区')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))

        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_to=from_to,
            nationality=nationality,
            info=info
        )
        return redirect(reverse('external_video'))

class VideoSubView(View):
    def get(self, request, video_id):
        if authenticate(request.user):
            video = Video.objects.get(pk=video_id)
            data = {}
            error = request.GET.get('error', '')
            data['error'] = error
            data['video'] = video
            return render_to_resoponse(request, 'dashboard/video/video_stub.html', data=data)

    def post(self, request, video_id):
        url = request.POST.get('url', '')
        video = Video.objects.get(pk=video_id)
        number = video.video_stub.count() + 1
        VideoStub.objects.create(video=video, url=url, number=number)
        return redirect(reverse('video_stub',kwargs={'video_id': video_id}))


class VideoStartView(View):
    def post(self, request):
        name = request.POST.get('name', '')
        identity = request.POST.get('identity', '')
        video_id = request.POST.get('video_id', '')

        #
        path_format = '{}'.format(reverse('video_stub', kwargs={'video_id': video_id}))

        #
        if not all(['name','identity','video_id']):
            return redirect('{}?error={}'.format(path_format, '缺少必要信息'))

        result = chekcAndGetVideoType(IdentityType,identity, '非法身份')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format, result['msg']))

        #主演与video_id做绑定
        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(
                name=name,
                identity=identity,
                video=video
            )
        except:
            return redirect('{}?error={}'.format(path_format, '创建失败'))
        return redirect(reverse('video_sub'), kwargs={'video_id': video_id})

class StarDelete(View):
    def get(self, request, star_id, video_id):
        Video.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub'), kwargs={'video_id': video_id})

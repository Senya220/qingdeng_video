from django.shortcuts import redirect, reverse
from django.views.generic import View
from libs.base_rander import render_to_resoponse
from django.contrib.auth import authenticate
from .models import Video, VideoSub, VideoStar, VideoType, FromType, NationalityType, IdentityType
from utils.common import chekcAndGetVideoType

# Create your views here.
# 外链视频视图
class ExternalVideo(View):
    def get(self, request):
        if authenticate(request.user):
            error = request.GET.get('error', '')
            data = {'error': error}
            # 查找用户自制视频之外的所有视频
            ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
            data['ex_videos'] = ex_videos

            #自制视频
            cus_videos = Video.objects.filter(from_to=FromType.custom.value)
            data['cus_videos'] = cus_videos

            return render_to_resoponse(request, 'dashboard/video/external_video.html',data=data)
        return redirect(reverse('dashboard_login'))

    def post(self, request):
        name = request.POST.get('name', '')
        image = request.POST.get('image', '')
        video_type = request.POST.get('video_type', '')
        from_to = request.POST.get('from_to', '')
        nationality = request.POST.get('nationaltity', '')
        info = request.POST.get('info', '')

        #通过video_id指定更改视频内容
        video_id = request.POST.get('video_id', '')
        #判断当前是否存在video_id，存在则修改
        if video_id:
            url_format = reverse('video_update', kwargs={'video_id': video_id})
        else:
            url_format = reverse('external_video')


        # 必填字段判断
        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(url_format, '缺少必要信息'))

        #视频验证
        result = chekcAndGetVideoType(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(url_format, result['msg']))

        # 视频来源
        result = chekcAndGetVideoType(FromType, from_to, '非法来源')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(url_format, result['msg']))

        #非法地区
        result = chekcAndGetVideoType(NationalityType, nationality, '非法地区')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))

        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=video_type,
                    from_to=from_to,
                    nationality=nationality,
                    info=info
                )
            except:
                return redirect(reverse('{}?error={}'.format(url_format, '创建失败')))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = image
                video.video_type = video_type
                video.nationality = nationality
                video.info = info
                video.save()
            except:
                return redirect(reverse('{}?error={}'.format(url_format, '更新失败')))
        return redirect(reverse('external_video'))

class VideoSubView(View):
    """
    控制视频类型和内容
    """
    def get(self, request, video_id):
        if authenticate(request.user):
            video = Video.objects.get(pk=video_id)
            data = {}
            error = request.GET.get('error', '')
            data['error'] = error
            data['video'] = video
            return render_to_resoponse(request, 'dashboard/video/video_sub.html', data=data)
        return redirect(reverse('dashboard_login'))

    # def post(self, request, video_id):
    #     url = request.POST.get('url', '')
    #     video = Video.objects.get(pk=video_id)
    #     number = video.video_stub.count() + 1
    #     VideoSub.objects.create(video=video, url=url, number=number)
    #     return redirect(reverse('video_stub',kwargs={'video_id': video_id}))


    def post(self, request, video_id):
        number = request.POST.get('number', '')
        videosub_id = request.POST.get('videosub_id', '')

        #判断当前视频是否为自制视频，自制视频这里是file 不是url
        url = request.POST.get('url', '')


        #url format
        url_format = reverse('video_sub', kwargs={'video_id': video_id})
        if not all([url,number]):
            return redirect('{}error={}'.format(url_format,'缺少必要信息'))
        # 获取视频信息 再去做更新 编辑
        video = Video.objects.get(pk=video_id)
        #判断当前是否由videosub_id ->yes update ; no create
        if not videosub_id:
            try:
                Video.objects.create(video=video, url=url, number=number)
            except:
                return redirect('{}error={}'.format(url_format, '创建失败'))
        else:
            video_sub = VideoSub.objects.get(pk=videosub_id)
            try:
                video_sub.url = url
                video_sub.number = number
                video_sub.save()
            except:
                return redirect('{}?error={}'.format(url_format, '更新失败'))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

class VideoStartView(View):
    def post(self, request):
        name = request.POST.get('name', '')
        identity = request.POST.get('identity', '')
        video_id = request.POST.get('video_id', '')

        #
        path_format = '{}'.format(reverse('video_sub', kwargs={'video_id': video_id}))

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
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

class StarDelete(View):
    def get(self, request, star_id, video_id):
        Video.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

class SubDelete(View):
    def get(self, request, videosub_id, video_id):
        Video.objects.filter(id=videosub_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

class VideoUpdate(View):
    def get(self, request, video_id):
        if authenticate(request.user):
            data = {}
            video = Video.objects.get('video_id', '')
            data['video'] = video
            return render_to_resoponse(request, 'dashboard/video/video_update.html', data=data)

class VideoUpdateStatus(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()
        return redirect(reverse('external_video'))

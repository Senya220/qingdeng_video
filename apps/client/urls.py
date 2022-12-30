
from django.urls import path
from .views import ExternalVideo, VideoSubView, VideoStartView, StarDelete, SubDelete, VideoUpdate, VideoUpdateStatus

urlpatterns = [
    path('video/external/', ExternalVideo.as_view(), name='external_video'),
    path('video/videosub/<intLvideo_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/star/', VideoStartView.as_view(), name='video_star'),
    path('video/star/delete/<int:star_id>/<int:video_id>', StarDelete.as_view(), name='star_delete'),
    path('video/sub/delete/<int:videosub_id>/<int:video_id>', SubDelete.as_view(), name='sub_delete'),
    path('video/update/<int:video_id>', VideoUpdate.as_view(), name='video_update'),
    path('video/update/status/<int:video_id>', VideoUpdateStatus.as_view(), name='update_status'),

]


from django.urls import path
from .views import ExternalVideo, VideoSubView, VideoStartView, StarDelete

urlpatterns = [
    path('video/external/', ExternalVideo.as_view(), name='external_video'),
    path('video/videosub/<intLvideo_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/star/', VideoStartView.as_view(), name='video_star'),
    path('video/star/delete<int:star_id>/<int:video_id>', StarDelete.as_view(), name='start_delete'),

]

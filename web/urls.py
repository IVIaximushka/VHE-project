from django.urls import path

from web.views import main_view, get_streaming_video, get_video, registration_view, authorization_view, channels_view, \
    channel_view, logout_view

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('authorization/', authorization_view, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('channels/', channels_view, name='channels'),
    path('channel/<int:user_id>/', channel_view, name='channel'),
    path('stream/<int:id>/', get_streaming_video, name='stream'),
    path('video/<int:id>/watch', get_video, name='video_watching'),
]

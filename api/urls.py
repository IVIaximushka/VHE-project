from django.urls import path

from api.views import start_view, video_view

urlpatterns = [
    path('start/', start_view, name='start'),
    path('videos/', video_view, name='videos')
]

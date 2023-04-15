from django.urls import path

from web.views import main_view, get_streaming_video, get_video, registration_view

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('stream/<int:id>/', get_streaming_video, name='stream'),
    path('<int:id>/', get_video, name='video'),
]

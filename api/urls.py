from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import start_view, video_view, user_profile_view, create_user_profile_view

urlpatterns = [
    path('start/', start_view, name='start'),
    path('videos/', video_view, name='videos'),
    path('token/', obtain_auth_token, name='token'),
    path('profile/', user_profile_view, name='profile'),
    path('profile/create', create_user_profile_view, name='create_profile')
]

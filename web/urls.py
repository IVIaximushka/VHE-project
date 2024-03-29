from django.urls import path

from web.views import main_view, get_streaming_video, get_video, registration_view, authorization_view, channels_view, \
    channel_view, logout_view, personal_account_view, load_video_view, chats, room, create_chat, enter_chat, my_chats, \
    edit_chat, admin_chat, ban

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('authorization/', authorization_view, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('personal_account/', personal_account_view, name='personal_account'),
    path('load_video/', load_video_view, name='load_video'),
    path('channels/', channels_view, name='channels'),
    path('channel/<int:user_id>/', channel_view, name='channel'),
    path('stream/<int:id>/', get_streaming_video, name='stream'),
    path('video/<int:id>/watch', get_video, name='video_watching'),
    path('create_chat/', create_chat, name='chat_creator'),
    path('chats/<int:id>/enter', enter_chat, name='enter_chat'),
    path('chats/', chats, name='chats'),
    path('chats/my', my_chats, name='my_chats'),
    path('chats/admin', admin_chat, name='admin_chats'),
    path('chats/<int:id>/edit', edit_chat, name='edit_chat'),
    path('chats/<int:chat_id>/edit/ban/<int:user_id>', ban, name='ban'),
    path('chats/<str:room_name>/', room, name="room"),
]

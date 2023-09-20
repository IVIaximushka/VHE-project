from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

from web.forms import RegistrationForm, AuthorizationForm, UpdateUserForm, UpdateProfileForm, LoadVideoForm, \
    CreateChatForm
from web.models import Video, User, UserProfile, Chat, ChatUser
from web.services import open_file


def main_view(request):
    return render(request, 'web/main.html', {'video_list': Video.objects.all()})


@login_required
def channels_view(request):
    author_list = UserProfile.objects.filter(is_author=True).select_related('user')
    return render(request, 'web/channels.html', {'author_list': author_list})


@login_required
def channel_view(request, user_id):
    author_video_list = Video.objects.filter(author_id=user_id).select_related('author')
    return render(request, 'web/main.html', {'video_list': author_video_list})


def registration_view(request):
    is_success = False
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_profile = UserProfile(
                user=user,
                is_author=form.cleaned_data['author'],
                avatar=form.cleaned_data['avatar']
            )
            user_profile.save()
            is_success = True
    return render(request, 'web/registration.html', {
        'form': form,
        'is_success': is_success
    })


def authorization_view(request):
    form = AuthorizationForm()
    if request.method == 'POST':
        form = AuthorizationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Введены неверные данные')
            else:
                login(request, user)
                return redirect('main')
    return render(request, 'web/authorization.html', {'form': form})


@login_required
def personal_account_view(request):
    profile = UserProfile.objects.get(user=request.user)
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    return render(request, 'web/personal_account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_author': profile.is_author
    })


@login_required
def load_video_view(request):
    profile = UserProfile.objects.get(user=request.user)
    video_form = LoadVideoForm()
    if request.method == 'POST':
        video_form = LoadVideoForm(request.POST, request.FILES)
        if video_form.is_valid():
            new_video = Video(
                title=video_form.cleaned_data['title'],
                video=video_form.cleaned_data['video'],
                preview=(video_form.cleaned_data['preview']
                         if video_form.cleaned_data['preview'] is not None
                         else 'preview/nopreview.jpg'),
                description=video_form.cleaned_data['description'],
                author=profile
            )
            new_video.save()
            return redirect('main')
    return render(request, 'web/load_video.html', {'video_form': video_form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def get_video(request, id):
    video = get_object_or_404(Video, id=id)
    video.views += 1
    video.save(update_fields=['views'])
    return render(request, 'web/video.html', {'video': video})


@login_required
def get_streaming_video(request, id: int):
    file, status_code, content_length, content_range = open_file(request, id)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


@login_required
def create_chat(request):
    is_success = False
    creation_form = CreateChatForm(instance=request.user)
    if request.method == 'POST':
        creation_form = CreateChatForm(request.POST, initial={'admin': request.user})
        if creation_form.is_valid():
            creation_form.save()
            new_user = ChatUser(
                chat=Chat.objects.filter(title=creation_form.instance.title).first(),
                user=request.user
            )
            new_user.save()
            is_success = True
    return render(request, "web/chat_creator.html", {
        'creation_form': creation_form,
        'is_success': is_success
    })


@login_required
def enter_chat(request, id):
    if len(ChatUser.objects.filter(chat_id=id, user=request.user)) == 0:
        new_user = ChatUser(
            chat_id=id,
            user=request.user
        )
        new_user.save()
    return redirect('chats')


@login_required
def chats(request):
    my_chats = list(ChatUser.objects.filter(user=request.user).values_list('chat_id'))
    my_chats = list(map(lambda x: x[0], my_chats))
    all_chats = Chat.objects.exclude(id__in=my_chats)
    return render(request, "web/all_chats.html", {
        'chats': all_chats
    })


@login_required
def my_chats(request):
    chats = list(ChatUser.objects.filter(user=request.user).values_list('chat_id'))
    chats = list(map(lambda x: x[0], chats))
    all_chats = Chat.objects.filter(id__in=chats)
    return render(request, "web/my_chats.html", {
        'chats': all_chats
    })


def room(request, room_name):
    return render(request, "web/room.html", {"room_name": room_name})

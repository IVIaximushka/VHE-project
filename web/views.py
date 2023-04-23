from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

from web.forms import RegistrationForm, AuthorizationForm
from web.models import Video, User, UserProfile
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

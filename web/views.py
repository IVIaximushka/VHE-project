from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404

from web.forms import RegistrationForm
from web.models import Video, User, UserProfile
from web.services import open_file


def main_view(request):
    return render(request, 'web/main.html', {'video_list': Video.objects.all()})


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


def get_video(request, id):
    _video = get_object_or_404(Video, id=id)
    return render(request, 'web/video.html', {'video': _video})


def get_streaming_video(request, id: int):
    file, status_code, content_length, content_range = open_file(request, id)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

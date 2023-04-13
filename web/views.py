from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404

from web.models import Video
from web.services import open_file


def main_view(request):
    return render(request, 'web/main.html', {'video_list': Video.objects.all()})


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

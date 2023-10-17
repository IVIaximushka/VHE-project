from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import VideoSerializer
from web.models import Video


@api_view(['GET'])
def start_view(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
def video_view(request):
    videos = Video.objects.all().select_related('author__user', 'genre')
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)

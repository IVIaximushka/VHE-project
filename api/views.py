from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.serializers import VideoSerializer, UserProfileSerializer
from web.models import Video, UserProfile


@api_view(['GET'])
@permission_classes([])
def start_view(request):
    return Response({'status': 'ok'})


@api_view(['GET', 'POST'])
def video_view(request):
    if request.method == 'POST':
        serializer = VideoSerializer(data=request.data,
                                     context={'request': request,
                                              'author': UserProfile.objects.filter(user=request.user).first()})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    videos = Video.objects.all().select_related('author__user', 'genre')
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_profile_view(request):
    profile = UserProfile.objects.filter(user=request.user).select_related('user')
    serializer = UserProfileSerializer(profile, many=True)
    return Response(serializer.data)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import json

from api.serializers import VideoSerializer, UserProfileSerializer, UserSerializer, GenreSerializer
from web.models import Video, UserProfile, Genre


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


@api_view(['POST'])
@permission_classes([])
def create_user_profile_view(request):
    user_serializer = UserSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.create(request.data)
    serializer = UserProfileSerializer(data=request.data,
                                       context={'request': request,
                                                'user': user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def genre_view(request):
    if request.method == 'POST':
        serializer = GenreSerializer(data=request.data,
                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

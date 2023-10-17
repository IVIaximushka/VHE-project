from rest_framework import serializers

from web.models import User, UserProfile, Genre


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    is_author = serializers.BooleanField()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title')


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    pub_date = serializers.DateTimeField()
    views = serializers.IntegerField()
    description = serializers.CharField()
    author = UserProfileSerializer()
    genre = GenreSerializer()

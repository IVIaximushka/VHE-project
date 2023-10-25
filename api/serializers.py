from rest_framework import serializers

from web.models import User, UserProfile, Genre, Video


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    avatar = serializers.ImageField()
    is_author = serializers.BooleanField()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title')


class VideoSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    # genre = GenreSerializer()

    def save(self, **kwargs):
        self.validated_data['author'] = self.context['author']
        return super().save(**kwargs)

    class Meta:
        model = Video
        fields = ('id', 'title', 'video', 'preview', 'description', 'author')

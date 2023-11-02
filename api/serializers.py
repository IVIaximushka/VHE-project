from rest_framework import serializers

from web.models import User, UserProfile, Genre, Video, Chat


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def save(self, **kwargs):
        self.validated_data['user'] = self.context['user']
        return super().save(**kwargs)

    class Meta:
        model = UserProfile
        fields = ('id', 'avatar', 'is_author', 'user')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title')


class ChatSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        if self.instance is None:
            self.validated_data['admin_id'] = self.context['admin']
        return super().save(**kwargs)

    class Meta:
        model = Chat
        fields = ('id', 'title', 'admin_id')


class VideoSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    # genre = GenreSerializer()

    def save(self, **kwargs):
        if self.instance is None:
            self.validated_data['author'] = self.context['author']
        return super().save(**kwargs)

    class Meta:
        model = Video
        fields = ('id', 'title', 'video', 'preview', 'description', 'author')

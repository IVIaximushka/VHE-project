from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватарка')
    is_author = models.BooleanField(default=False, verbose_name='Автор')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Application(models.Model):
    description = models.CharField(max_length=500, default=None, verbose_name='Описание')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Genre(models.Model):
    title = models.CharField(max_length=15, null=False, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Video(models.Model):
    title = models.CharField(max_length=40, null=False, verbose_name='Название')
    video = models.FileField(upload_to='video/',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                             verbose_name='Видео')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    preview = models.ImageField(upload_to='preview/', null=True, blank=True, verbose_name='Превью')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    description = models.CharField(max_length=500, null=True, default=None, verbose_name='Описание')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Автор')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name='Жанр')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

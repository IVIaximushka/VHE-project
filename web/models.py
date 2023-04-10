from django.db import models
from django.contrib.auth.models import User


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


class Genre(models.Model):
    title = models.CharField(max_length=15, null=False, verbose_name='Название')


class Video(models.Model):
    title = models.CharField(max_length=40, null=False, verbose_name='Название')
    video = models.CharField(max_length=40, null=False, verbose_name='Путь')
    pub_date = models.DateField(null=False, verbose_name='Дата публикации')
    preview = models.ImageField(null=False, verbose_name='Превью')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    description = models.CharField(max_length=500, default=None, verbose_name='Описание')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Автор')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, verbose_name='Жанр')

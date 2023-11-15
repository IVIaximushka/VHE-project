import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.files import File

from web.models import Genre, User, UserProfile, Chat, Video


class GenreTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='max', password='123',
                                        email='t@t.ru', is_active=True)
        self.genre = Genre.objects.create(title='genre1')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_genre_create(self):
        response = self.client.post(reverse('genre-list'),
                                    headers={'Authorization': f'Token {self.token.key}'},
                                    data={'title': 'genre2'})
        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_list(self):
        response = self.client.get(reverse('genre-list'),
                                   headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_delete(self):
        response = self.client.delete(reverse('genre-detail', kwargs={'pk': self.genre.id}),
                                      headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(Genre.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_genre_update(self):
        response = self.client.put(reverse('genre-detail', kwargs={'pk': self.genre.id}),
                                   headers={'Authorization': f'Token {self.token.key}'},
                                   data={'title': 'new_title'})
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Genre.objects.get(id=self.genre.id).title, 'new_title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='max', password='123',
                                        email='t@t.ru', is_active=True)
        self.user_profile = UserProfile.objects.create(user=self.user, is_author=True)
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_user_profile_create(self):
        response = self.client.post(reverse('create_profile'),
                                    data={'username': 'test',
                                          'email': '123@mail.ru',
                                          'password': '123',
                                          'is_author': 'True'})
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_profile_list(self):
        response = self.client.get(reverse('profile'),
                                   headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChatTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='max', password='123',
                                        email='t@t.ru', is_active=True)
        self.chat = Chat.objects.create(admin=self.user, title='chat')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_chat_create(self):
        response = self.client.post(reverse('chat-list'),
                                    headers={'Authorization': f'Token {self.token.key}'},
                                    data={'title': 'test_chat'})
        self.assertEqual(Chat.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_chat_list(self):
        response = self.client.get(reverse('chat-list'),
                                   headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_delete(self):
        response = self.client.delete(reverse('chat-detail', kwargs={'pk': self.chat.id}),
                                      headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(Chat.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_chat_update(self):
        response = self.client.put(reverse('chat-detail', kwargs={'pk': self.chat.id}),
                                   headers={'Authorization': f'Token {self.token.key}'},
                                   data={'title': 'new_title'})
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Chat.objects.get(id=self.chat.id).title, 'new_title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VideoTests(APITestCase):
    def setUp(self) -> None:
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.mp4'

        self.user = User.objects.create(username='max', password='123',
                                        email='t@t.ru', is_active=True)
        self.user_profile = UserProfile.objects.create(user=self.user, is_author=True)
        self.genre = Genre.objects.create(title='genre1')
        self.video = Video.objects.create(title='test', video=file_mock.name,
                                          author=self.user_profile, genre=self.genre)
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_video_list(self):
        response = self.client.get(reverse('video-list'),
                                   headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_create(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'video.mp4'
        response = self.client.post(reverse('video-list'),
                                    headers={'Authorization': f'Token {self.token.key}'},
                                    data={'title': 'video', 'video': file_mock,
                                          'author': self.user_profile, 'genre': self.genre})
        self.assertEqual(Video.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_video_delete(self):
        response = self.client.delete(reverse('video-detail', kwargs={'pk': self.video.id}),
                                      headers={'Authorization': f'Token {self.token.key}'})
        self.assertEqual(Video.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_video_update(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'video.mp4'
        response = self.client.put(reverse('video-detail', kwargs={'pk': self.video.id}),
                                   headers={'Authorization': f'Token {self.token.key}'},
                                   data={'title': 'new_title',
                                         'video': file_mock})
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(Video.objects.get(id=self.video.id).title, 'new_title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

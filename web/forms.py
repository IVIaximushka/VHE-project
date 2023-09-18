import re

from django import forms

from web.models import User, UserProfile, Video


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Электропочта:")
    username = forms.CharField(label="Имя пользователя:")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-field"}), label="Пароль:")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-field"}), label="Повторите пароль:")
    author = forms.BooleanField(initial=False, required=False, label="Автор:")
    avatar = forms.ImageField(required=False, label="Аватар:")
    avatar.widget.attrs.update({"class": "center"})
    email.widget.attrs.update({"class": "form-field"})
    username.widget.attrs.update({"class": "form-field"})

    def clean(self):
        cleaned_data = super().clean()
        if not re.search(r'^(?=.*\W)(?=.*\D)(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$',
                         cleaned_data['password']):
            self.add_error('password', 'Пароль слишком простой! '
                                       'Он должен включать в себя '
                                       'как минимум одну заглавную латинскую букву, '
                                       'одну строчную, одну цифру и один небуквенный '
                                       'и нецифровой символ. '
                                       'Количество символов в пароле '
                                       'должно быть от 8 до 15.')
        elif cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password2', 'Пароли не совпадают!')
        elif User.objects.filter(username=cleaned_data['username']).exists():
            self.add_error('username', 'Пользователь с таким именем уже существует!')
        elif User.objects.filter(email=cleaned_data['email']).exists():
            self.add_error('email', 'Пользователь с такой почтой уже существует!')
        return cleaned_data


class AuthorizationForm(forms.Form):
    username = forms.CharField(label="Имя пользователя:")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-field"}), label="Пароль:")
    username.widget.attrs.update({"class": "form-field"})


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(label="Поменять имя пользователя:",
                               widget=forms.TextInput(attrs={'class': 'form-field form-control'}))

    class Meta:
        model = User
        fields = ['username', ]


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, label="Выбрать новую аватарку:",
                              widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProfile
        fields = ['avatar', ]


class LoadVideoForm(forms.Form):
    title = forms.CharField(label='Название')
    video = forms.FileField(label='Видео',
                            widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    preview = forms.ImageField(label='Превью', required=False, initial=None)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={"class": "form-field"}))
    title.widget.attrs.update({"class": "form-field"})


class CreateChatForm(forms.ModelForm):
    pass

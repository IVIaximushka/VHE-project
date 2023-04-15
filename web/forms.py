import re

from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    author = forms.BooleanField(initial=False, required=False)
    avatar = forms.ImageField(required=False)

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
        return cleaned_data

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=True, max_length=100)
    last_name = forms.CharField(label='Фамилия', required=True, max_length=100)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'group',
        )


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', required=True, max_length=100)
    last_name = forms.CharField(label='Фамилия', required=True, max_length=100)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'group',
        )

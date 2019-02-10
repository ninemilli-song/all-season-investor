from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    mobile = forms.RegexField(regex=r'^1(3|4|5|7|8)\d{9}$', help_text="Phone number")

    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'password1', 'password2', )
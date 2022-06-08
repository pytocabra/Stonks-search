from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.forms import UserCreationForm


# modified user register form to require email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Idk how to add placeholders to inputs - code below doesnt work :<

# class UserLoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'placeholder': 'Username here',
#             })
#         }



import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, AccountDetails, UserAddress
from django.contrib.auth.forms import UserChangeForm





class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",

            "email",
            "password1",
            "password2",
        ]


class AccountDetailsForm(forms.ModelForm):



    class Meta:
        model = AccountDetails
        fields = [

            'picture'
        ]
        widgets = {
            'picture': forms.ClearableFileInput(),
        }







class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'required': True,
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'required': True,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Character, Item



class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'hero_class']





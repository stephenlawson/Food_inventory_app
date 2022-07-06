from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'captcha']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weekly_email_updates', 'image']
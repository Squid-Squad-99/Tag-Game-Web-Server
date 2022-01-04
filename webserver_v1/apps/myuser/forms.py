from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username',)


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', )
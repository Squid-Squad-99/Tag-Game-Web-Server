from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class MyUserCreationForm(UserCreationForm):
    birth_day = forms.DateField(help_text=_('Required. Format: YYYY-MM-DD'))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'birth_day', )


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'birth_day', )
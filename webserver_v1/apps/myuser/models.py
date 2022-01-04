from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
import uuid
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('can_hold_activity', False)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,  password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('can_hold_activity', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    # username as default value
    username = models.CharField(unique=True, max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # whether is superuser to reach admin page
    is_superuser = models.BooleanField(default=False)
    # whether the user can hold activity
    can_hold_activity = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

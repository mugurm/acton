import warnings

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import SiteProfileNotAvailable
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote


class Error(Exception):
    pass

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if 'username' in extra_fields:
            del extra_fields['username']
        u = self.create_user(email=email, password=password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class User(AbstractUser):
    remote_user = models.BooleanField(default=False)

    @classmethod
    def get_or_create_remote_user(cls, user_id):
        if "@" not in user_id:
            raise Error('user_id should be of the form of an email')

        username, domain = map(lambda x: x.strip(), user_id.split('@'))
        if domain in settings.DOMAINS:
            try:
                user, created = User.objects.get(username=username)
            except User.DoesNotExist:
                raise Error('User is not external user and doesn\'t exist on our db')
            else:
                return user
        else:
            user, created = User.objects.get_or_create(username=user_id, remote=True)
        return user

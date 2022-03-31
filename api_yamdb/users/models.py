
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .enums import Role


class CustomUser(AbstractBaseUser):
    """Class CustomUser."""

    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=128,blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(black=True)
    role = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in Role],
        default=Role.USER
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=128,blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

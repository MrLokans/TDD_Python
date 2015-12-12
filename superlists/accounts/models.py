from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.EmailField()
    last_login = models.DateTimeField(default=timezone.now)
    # w/o that hack django auth want work
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'


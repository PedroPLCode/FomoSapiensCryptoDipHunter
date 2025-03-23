from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    telegram_chat_id = models.CharField(max_length=512, blank=True, null=True)
    telegram_signals_receiver = models.BooleanField(default=True)
    email_signals_receiver = models.BooleanField(default=True)

    def __str__(self):
        return self.username

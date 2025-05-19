import json
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class PasswordResetToken(models.Model):
    reset_token = models.CharField(max_length=256)
    change_counter = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, related_name='reset_token', on_delete=models.CASCADE)

    def password_changed(self):
        self.change_counter += 1
        self.save()

        self.user.profile.last_password_change = timezone.now()
        self.user.profile.save()
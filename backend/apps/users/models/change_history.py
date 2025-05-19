import json
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="change_history")
    field_name = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} zmienił {self.field_name} z {self.old_value} na {self.new_value} ({self.changed_at})"
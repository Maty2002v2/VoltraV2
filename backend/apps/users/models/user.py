from datetime import timedelta
import json
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from apps.users.models.password_reset import PasswordResetToken
from apps.users.utils import reset_password_token
from apps.users.utils.send_mail import send_reset_password_mail
from apps.users.models.change_history import ChangeHistory
User = get_user_model()


class UserProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_password_change = models.DateTimeField(auto_now_add=True)
    invalid_login_attempts = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Numer telefonu użytkownika")
    client_number = models.CharField(max_length=50, blank=True, null=True, help_text="Numer klienta użytkownika")

    NOTIFICATION_METHODS = [
        ('email', 'E-mail'),
        ('sms', 'SMS'),
        ('webpush', 'Web Push'),
    ]
    notification_preferences = models.JSONField(default=list,
                                                help_text="Preferowane metody powiadomień (e-mail, SMS, Web Push)")
    okaycrm_id = models.CharField(max_length=50, blank=True, null=True)

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = UserProfile.objects.get(pk=self.pk)
            changed_fields = {}

            for field in ['phone_number', 'client_number', 'notification_preferences']:
                old_value = getattr(old_instance, field)
                new_value = getattr(self, field)
                if old_value != new_value:
                    changed_fields[field] = {"old": old_value, "new": new_value}

            super().save(*args, **kwargs)

            for field, values in changed_fields.items():
                ChangeHistory.objects.create(
                    user=self.user,
                    field_name=field,
                    old_value=json.dumps(values['old'], ensure_ascii=False),
                    new_value=json.dumps(values['new'], ensure_ascii=False),
                )
        else:
            super().save(*args, **kwargs)




    def reset_invalid_login_attempts(self):
        self.invalid_login_attempts = 0
        self.save()

    @classmethod
    def validate_invalid_attempts(cls, user):
        user_profile, _ = cls.objects.get_or_create(user=user)
        if user_profile.invalid_login_attempts >= settings.INVALID_LOGIN_ATTEMPTS:
            user.is_active = False
            user.save()
            raise AuthenticationFailed(detail='User is locked', code='user_locked')
        user_profile.invalid_login_attempts += 1
        user_profile.save()

    @classmethod
    def validate_last_password_change(cls, user):
        user_profile, _ = cls.objects.get_or_create(user=user)
        max_date = user_profile.last_password_change + timedelta(days=settings.PASSWORD_LIFESPAN_DAYS)
        if timezone.now() > max_date:
            token = reset_password_token.make_token(user)
            password_reset, _ = PasswordResetToken.objects.get_or_create(
                user=user,
            )
            password_reset.reset_token = token
            password_reset.save()
            send_reset_password_mail(user, token)
            raise AuthenticationFailed(detail='Password expired', code='password_expired')



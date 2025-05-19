from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError


class PasswordSerializer(serializers.Serializer):
    new_password = fields.CharField()
    password_confirmation = fields.CharField()

    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        check = self.initial_data.get('new_password') == self.initial_data.get('password_confirmation')
        if raise_exception and not check:
            raise ValidationError(
                {'password_confirmation': ['Passwords not match']},
            )
        return check

from rest_framework.exceptions import PermissionDenied

from apps.users.models.password_reset import PasswordResetToken
from apps.users.utils import reset_password_token


class ValidateTokenByHash(object):
    @staticmethod
    def validate_token_by_hash(user_hash):
        try:
            password_reset = PasswordResetToken.objects.get(reset_token=user_hash)
        except PasswordResetToken.DoesNotExist:
            raise PermissionDenied(detail='Invalid hash')

        user = password_reset.user
        if not reset_password_token.check_token(user, user_hash):
            raise PermissionDenied(detail='Invalid hash')

        return password_reset

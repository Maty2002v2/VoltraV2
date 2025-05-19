from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            user.pk + timestamp + user.is_active,
        )


reset_password_token = ResetPasswordTokenGenerator()

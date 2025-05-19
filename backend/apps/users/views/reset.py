from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.users.models.password_reset import PasswordResetToken
from apps.users.serializers import EmailSerializer
from apps.users.utils import reset_password_token
from apps.users.utils.send_mail import send_reset_password_mail

User = get_user_model()


class ResetPasswordView(APIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = EmailSerializer

    def post(self, request):
        email = request.data.get('email')
        self.serializer_class(data=request.data).is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=email)
            token = reset_password_token.make_token(user)
            password_reset, _ = PasswordResetToken.objects.get_or_create(
                user=user,
            )
            password_reset.reset_token = token
            password_reset.save()

            send_reset_password_mail(user, token)
        except User.DoesNotExist:
            pass  # nice try hacker :keku:

        return Response({'send to': email}, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers.password import PasswordSerializer
from apps.users.views.mixins.validate_token import ValidateTokenByHash


class ChangePasswordView(APIView, ValidateTokenByHash):
    serializer_class = PasswordSerializer

    def post(self, request, user_hash):
        new_password = request.data.get('new_password')
        self.serializer_class(data=request.data).is_valid(raise_exception=True)

        password_reset = self.validate_token_by_hash(user_hash)
        user = password_reset.user

        user.set_password(new_password)
        user.save()
        password_reset.password_changed()
        return Response(status=status.HTTP_200_OK)

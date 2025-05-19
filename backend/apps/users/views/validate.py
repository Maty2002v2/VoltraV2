from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import HashSerializer
from apps.users.utils import reset_password_token
from apps.users.views.mixins.validate_token import ValidateTokenByHash


class ValidatePasswordView(APIView, ValidateTokenByHash):
    serializer_class = HashSerializer

    def post(self, request):
        user_hash = request.data.get('hash')
        self.serializer_class(data=request.data).is_valid(raise_exception=True)

        password_reset = self.validate_token_by_hash(user_hash)

        new_reset_token = reset_password_token.make_token(password_reset.user)
        password_reset.reset_token = new_reset_token
        password_reset.save()
        return Response({'hash': new_reset_token}, status=status.HTTP_200_OK)

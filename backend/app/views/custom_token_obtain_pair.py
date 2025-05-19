from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView

from app.serializers.custom_token_obtain_pair import CustomTokenObtainPairSerializer
from apps.users.models import UserProfile

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = request.data.get('username')
        if not username:
            raise ValidationError('Username is required')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed(detail='Invalid credentials', code='invalid_credentials')

        UserProfile.validate_last_password_change(user)

        try:
            serializer.is_valid(raise_exception=True)
            user.profile.reset_invalid_login_attempts()
        except Exception:
            UserProfile.validate_invalid_attempts(user)
            raise AuthenticationFailed(detail='Invalid credentials', code='invalid_credentials')

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

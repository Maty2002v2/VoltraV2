from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy
from rest_framework.exceptions import AuthenticationFailed

from app.serializers.custom_token_obtain_pair import CustomTokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializerTestCase(TestCase):
    def test_get_token(self):
        user = mommy.make(User)
        token = CustomTokenObtainPairSerializer.get_token(user=user)

        assert token
        assert token['is_superuser'] == user.is_superuser

    def test_validate_user_success(self):
        username = 'username'
        password = 'users'
        User.objects.create_user(
            username=username,
            password=password,
        )
        payload = {
            'username': username,
            'users': password,
        }
        serializer = CustomTokenObtainPairSerializer(data=payload)

        assert serializer.is_valid()

    def test_validate_user_not_active(self):
        username = 'username'
        password = 'users'
        User.objects.create_user(
            username=username,
            password=password,
            is_active=False,
        )
        payload = {
            'username': username,
            'users': password,
        }
        serializer = CustomTokenObtainPairSerializer(data=payload)

        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid()

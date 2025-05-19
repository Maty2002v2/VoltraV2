from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status

from app.tests.user_factories import make_user
from apps.users.models.password_reset import PasswordResetToken
from apps.users.utils import reset_password_token
from apps.users.views import ValidatePasswordView


class ValidateHashTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.view_obtain = ValidatePasswordView
        self.url_obtain = reverse('validate_hash')

    def test_validate_no_data(self):
        # WHEN
        request = self.factory.post(path=self.url_obtain)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_fake_data(self):
        # GIVEN
        data = {
            'hash': 'Foo',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_validate_true_data(self):
        # GIVEN
        username = 'username'
        password = 'users'
        email = 'username@users.com'
        user = make_user(username=username, password=password, email=email)
        token = reset_password_token.make_token(user)
        PasswordResetToken.objects.create(user=user, reset_token=token)
        data = {
            'hash': token,
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('hash')

    def test_validate_invalid_data(self):
        # GIVEN
        username = 'username'
        password = 'users'
        email = 'username@users.com'
        user = make_user(username=username, password=password, email=email)
        token = reset_password_token.make_token(user)
        data = {
            'hash': token,
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_403_FORBIDDEN

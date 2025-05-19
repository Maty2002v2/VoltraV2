from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status

from app.tests.user_factories import make_user
from apps.users.models import UserProfile
from apps.users.models.password_reset import PasswordResetToken
from apps.users.utils import reset_password_token
from apps.users.views import ChangePasswordView


class ChangePasswordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.view_obtain = ChangePasswordView
        self.url_obtain = reverse('validate_hash')

    def test_change_no_data(self):
        # WHEN
        request = self.factory.post(path=self.url_obtain)
        response = self.view_obtain.as_view()(request, user_hash='Foo')
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_fake_data(self):
        # GIVEN
        data = {
            'new_password': 'Foo',
            'password_confirmation': 'Foo',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request, user_hash='Foo')
        # THEN
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_change_validate_passwords(self):
        # GIVEN
        username = 'username'
        password = 'users'
        email = 'username@users.com'
        user = make_user(username=username, password=password, email=email)
        token = reset_password_token.make_token(user)
        PasswordResetToken.objects.create(user=user, reset_token=token)
        data = {
            'new_password': 'Foo',
            'password_confirmation': 'Bar',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request, user_hash=token)
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_true_data(self):
        # GIVEN
        username = 'username'
        password = 'users'
        email = 'username@users.com'
        user = make_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user)
        token = reset_password_token.make_token(user)
        PasswordResetToken.objects.create(user=user, reset_token=token)
        data = {
            'new_password': 'Foo',
            'password_confirmation': 'Foo',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request, user_hash=token)
        # THEN
        assert response.status_code == status.HTTP_200_OK

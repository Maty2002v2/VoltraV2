from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status

from app.tests.user_factories import make_user
from apps.users.views import ResetPasswordView


class ResetPasswordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.view_obtain = ResetPasswordView
        self.url_obtain = reverse('reset_password')

    def test_reset_no_data(self):
        # WHEN
        request = self.factory.post(path=self.url_obtain)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reset_bad_email(self):
        # GIVEN
        data = {
            'email': 'Foo',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reset_fake_data(self):
        # GIVEN
        data = {
            'email': 'Foo@Bar.com',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_200_OK

    def test_reset_true_user(self):
        # GIVEN
        username = 'username'
        password = 'users'
        email = 'username@users.com'
        make_user(username=username, password=password, email=email)
        data = {
            'email': email,
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_200_OK

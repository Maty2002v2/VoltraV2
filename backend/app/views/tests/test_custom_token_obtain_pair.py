from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from app.tests.user_factories import make_user
from app.views.custom_token_obtain_pair import CustomTokenObtainPairView


class CustomTokenObtainPairTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.view_obtain = CustomTokenObtainPairView
        self.url_obtain = reverse('token_obtain_pair')

        self.view_refresh = TokenRefreshView
        self.url_refresh = reverse('token_obtain_pair')

    def test_obtain_no_credentials(self):
        # WHEN
        request = self.factory.post(path=self.url_obtain)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_obtain_no_user(self):
        # GIVEN
        data = {
            'username': 'Foo',
            'users': 'Bar',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_obtain_wrong_credentials(self):
        # GIVEN
        username = 'username'
        password = 'users'
        make_user(username=username, password=password)
        data = {
            'username': 'username',
            'users': 'Bar',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_obtain_success(self):
        # GIVEN
        username = 'username'
        password = 'users'
        user = make_user(username=username, password=password)
        data = {
            'username': user,
            'users': password,
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        response = self.view_obtain.as_view()(request)
        # THEN
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.status_code == status.HTTP_200_OK

    def test_refresh_no_token(self):
        # WHEN
        request = self.factory.post(path=self.url_refresh)
        response = self.view_refresh.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_refresh_wrong_token(self):
        # GIVEN
        data = {
            'refresh': 'FooBar',
        }
        # WHEN
        request = self.factory.post(path=self.url_refresh, data=data)
        response = self.view_refresh.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_success(self):
        # GIVEN
        user = make_user()
        refresh = RefreshToken.for_user(user=user)
        data = {
            'refresh': str(refresh),
        }
        # WHEN
        request = self.factory.post(path=self.url_refresh, data=data)
        response = self.view_refresh.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_200_OK

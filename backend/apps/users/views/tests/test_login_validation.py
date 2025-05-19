from datetime import timedelta

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from app.tests.user_factories import make_user
from app.views.custom_token_obtain_pair import CustomTokenObtainPairView
from apps.users.models import UserProfile


class LoginValidationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.view_obtain = CustomTokenObtainPairView
        self.url_obtain = reverse('token_obtain_pair')

    def test_too_many_wrong_credentials(self):
        # GIVEN
        username = 'username'
        password = 'users'
        make_user(username=username, password=password)
        data = {
            'username': username,
            'users': 'Bar',
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        for _ in range(5):
            self.view_obtain.as_view()(request)

        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'User is locked'

    def test_wrong_last_password_change_date(self):
        # GIVEN
        username = 'username'
        password = 'users'
        user = make_user(username=username, password=password)
        data = {
            'username': username,
            'users': password,
        }
        # WHEN
        request = self.factory.post(path=self.url_obtain, data=data)
        self.view_obtain.as_view()(request)
        profile = UserProfile.objects.get(user=user)
        profile.last_password_change = timezone.now() - timedelta(days=100)
        profile.save()
        response = self.view_obtain.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'Password expired'

from django.test import RequestFactory, TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from app.tests.user_factories import make_user
from apps.points.models import Tag
from apps.points.views import TagListView


class TagListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = TagListView
        self.url = reverse('tag')
        self.user = make_user()
        self.refresh = RefreshToken.for_user(self.user)

    def test_get_no_credentials(self):
        # WHEN
        request = self.factory.get(path=self.url)
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_success(self):
        # GIVEN
        tag = mommy.make(_model=Tag)
        # WHEN
        request = self.factory.get(
            path=self.url,
            HTTP_AUTHORIZATION='Token {token}'.format(token=self.refresh.access_token),
        )
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count']
        results = dict(response.data['results'][0])
        assert results == {'id': tag.id, 'name': tag.name}

    def test_post_no_credentials(self):
        # WHEN
        request = self.factory.post(path=self.url)
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_success(self):
        # GIVEN
        name = 'FooBar'
        data = {'name': name}
        # WHEN
        request = self.factory.post(
            path=self.url,
            HTTP_AUTHORIZATION='Token {token}'.format(token=self.refresh.access_token),
            data=data,
        )
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == name

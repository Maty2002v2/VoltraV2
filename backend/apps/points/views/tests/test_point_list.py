from django.test import RequestFactory, TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from app.tests.user_factories import make_user
from apps.division.models import Division
from apps.points.models import Point
from apps.points.serializers import PointDetailSerializer, PointListSerializer
from apps.points.views import PointListView


class PointListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = PointListView
        self.url = reverse('point')
        self.user = make_user()
        self.refresh = RefreshToken.for_user(self.user)

    def test_point_no_credentials(self):
        # WHEN
        request = self.factory.get(path=self.url)
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_success(self):
        # GIVEN
        division = mommy.make(_model=Division, account=self.user)
        point = mommy.make(_model=Point, division=division, verified=True)
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
        assert results == PointListSerializer(instance=point).data

    def test_get_multiple_points(self):
        # GIVEN
        quantity = 100
        division = mommy.make(_model=Division, account=self.user)
        mommy.make(_model=Point, division=division, verified=True, _quantity=quantity)
        # WHEN
        request = self.factory.get(
            path=self.url,
            HTTP_AUTHORIZATION='Token {token}'.format(token=self.refresh.access_token),
        )
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == quantity

    def test_post_no_credentials(self):
        # WHEN
        request = self.factory.post(path=self.url)
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_success(self):
        # GIVEN
        mommy.make(_model=Division, account=self.user)
        data = {
            'city': '',
            'contract_duration': '',
            'contract_type': '',
            'counter_number': '',
            'name': 'test',
            'notice_period': '',
            'osd_next': '',
            'osd_number': '',
            'post': '',
            'power': '',
            'ppe_number': '',
            'sale_end': None,
            'sale_start': None,
            'seller': '',
            'street': '',
            'street_number': '',
            'tags': [],
            'tariff': '',
            'termination_date': None,
            'zip_code': '',
        }
        # WHEN
        request = self.factory.post(
            path=self.url,
            HTTP_AUTHORIZATION='Token {token}'.format(token=self.refresh.access_token),
            data=data,
            content_type='application/json',
        )
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_validation(self):
        # GIVEN
        mommy.make(_model=Division, account=self.user)
        data = {
            'city': '',
            'contract_duration': '',
            'contract_type': '',
            'counter_number': '',
            'name': '',
            'notice_period': '',
            'osd_next': '',
            'osd_number': '',
            'post': '',
            'power': '',
            'ppe_number': '',
            'sale_end': None,
            'sale_start': None,
            'seller': '',
            'street': '',
            'street_number': '',
            'tags': [],
            'tariff': '',
            'termination_date': None,
            'zip_code': '12345678910',
        }
        # WHEN
        request = self.factory.post(
            path=self.url,
            HTTP_AUTHORIZATION='Token {token}'.format(token=self.refresh.access_token),
            data=data,
            content_type='application/json',
        )
        response = self.view.as_view()(request)
        # THEN
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert PointDetailSerializer.POINT_NAME_VALIDATION_ERROR in response.data['errors']
        assert len(response.data['errors']) == 1

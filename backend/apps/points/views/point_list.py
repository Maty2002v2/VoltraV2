from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from apps.points.filters import PointCostFilter, PointFilter
from apps.points.serializers import PointDetailSerializer, PointListSerializer
from apps.points.views import PointAPIView


class PointListView(PointAPIView, ListCreateAPIView):
    serializer_class = PointListSerializer
    filterset_class = PointFilter

    def get_queryset(self):
        return self.queryset.filter(verified=True, division__account_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        qs = self.filter_queryset(self.get_queryset())

        usage = 0
        costs = 0
        for point in qs:
            for point_filter in PointCostFilter(request.GET).qs.filter(point_id=point.pk):
                usage += point_filter.usage
                costs += point_filter.brutto

        response.data['total_costs'] = {
            'usage': usage,
            'costs': costs,
        }
        return response

    def post(self, request, *args, **kwargs):
        serializer = PointDetailSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

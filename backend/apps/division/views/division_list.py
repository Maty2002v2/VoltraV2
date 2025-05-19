from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication

from apps.division.filters import DivisionFilter
from apps.division.models import Division
from apps.division.serializers import DivisionListSerializer
from apps.points.filters import PointCostFilter


class DivisionListView(ListAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionListSerializer
    authentication_classes = [authentication.JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DivisionFilter

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        qs = self.filter_queryset(self.get_queryset())

        usage = 0
        costs = 0
        for division in qs:
            for point in division.points.all():
                for point_cost in PointCostFilter(request.GET).qs.filter(point_id=point.pk):
                    usage += point_cost.usage
                    costs += point_cost.brutto

        response.data['total_costs'] = {
            'usage': usage,
            'costs': costs,
        }
        return response

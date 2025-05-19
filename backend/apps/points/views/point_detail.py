from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from apps.points.filters import PointCostFilter
from apps.points.serializers import PointDetailSerializer
from apps.points.views import PointAPIView


class PointDetailView(PointAPIView, RetrieveUpdateAPIView):
    serializer_class = PointDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = Response(serializer.data)
        costs = PointCostFilter(request.GET).qs.filter(point_id=instance.pk)
        response.data['total_costs'] = {
            'usage': sum([cost.usage for cost in costs]),
            'costs': sum([cost.brutto for cost in costs]),
        }
        return response

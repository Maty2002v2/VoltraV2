from rest_framework import serializers

from apps.points.filters import PointCostFilter
from apps.points.models import PointCost


class PointCostSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PointCost
        exclude = ('created_at', 'modified_at')


class PointCostsSerializer(serializers.ModelSerializer):
    costs = serializers.SerializerMethodField()

    def get_costs(self, obj):
        request = self.context.get('request')
        data = request.GET if request else {}
        costs = PointCostFilter(data).qs.filter(point_id=obj.pk)
        return PointCostSerializer(costs, many=True).data

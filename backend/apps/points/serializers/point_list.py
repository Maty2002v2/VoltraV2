from apps.points.models import Point
from apps.points.serializers.point_costs import PointCostsSerializer
from apps.points.serializers.point_tags import PointTagsSerializer


class PointListSerializer(PointCostsSerializer, PointTagsSerializer):
    class Meta(object):
        model = Point
        fields = ('id', 'name', 'tags', 'costs')

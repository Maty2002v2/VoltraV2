from rest_framework import serializers

from apps.division.models import Division
from apps.points.serializers import PointDetailSerializer


class DivisionDetailSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()

    def get_points(self, obj):
        points = obj.points.filter(verified=True)
        return PointDetailSerializer(points, many=True).data

    class Meta(object):
        model = Division
        fields = '__all__'

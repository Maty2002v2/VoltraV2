from rest_framework import serializers

from apps.points.models import Tag


class PointTagsSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

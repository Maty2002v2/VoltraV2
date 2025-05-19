from rest_framework import serializers

from apps.points.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

from rest_framework import serializers

from apps.division.models import Division


class DivisionListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Division
        fields = '__all__'

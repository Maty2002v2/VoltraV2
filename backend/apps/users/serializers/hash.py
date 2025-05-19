from rest_framework import fields, serializers


class HashSerializer(serializers.Serializer):
    hash = fields.CharField()

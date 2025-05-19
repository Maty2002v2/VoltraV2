from rest_framework import fields, serializers


class EmailSerializer(serializers.Serializer):
    email = fields.EmailField()

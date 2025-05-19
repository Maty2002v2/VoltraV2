from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    divisions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(object):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'divisions')

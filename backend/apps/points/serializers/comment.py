from rest_framework import serializers

from apps.points.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Comment
        fields = '__all__'

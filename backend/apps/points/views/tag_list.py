from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication

from apps.points.models import Tag
from apps.points.serializers import TagSerializer


class TagListView(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.order_by('name').all()
    authentication_classes = [authentication.JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

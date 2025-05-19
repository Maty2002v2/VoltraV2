from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication

from app.serializers.user_info import UserInfoSerializer


class UserInfoView(RetrieveAPIView):
    authentication_classes = [authentication.JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return get_user_model().objects.get(pk=self.request.user.pk)

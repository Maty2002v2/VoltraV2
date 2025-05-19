from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication

from apps.division.models import Division
from apps.division.serializers import DivisionDetailSerializer


class DivisionDetailView(RetrieveAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionDetailSerializer
    authentication_classes = [authentication.JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

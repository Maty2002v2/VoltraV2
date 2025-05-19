from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication


from rest_framework.views import APIView
from ..models import Point, PointCostProxy
from datetime import datetime
class PointAPIView(object):
    queryset = Point.objects.order_by('id').all()
    authentication_classes = [authentication.JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    query_parameters = ['costs_date_before', 'costs_date_after']


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


from ..models import PointProxyRaport
from apps.common.utils.excel_export import export

# class ExportUserCosts(APIView):
#     """
#     Klasa widoku DRF, która zwraca raport Excel z punktami
#     przypisanymi do zalogowanego użytkownika.
#     """
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         if not request.user.is_authenticated:
#             return Response('Musisz być zalogowany!', status=403)
#
#         queryset = PointProxyRaport.objects.filter(division__account=request.user)
#
#         file_path = 'app/templates/excel_cost_template.xlsx'
#         response = export(request, file_path, 'costs', queryset, start_row=1, index_column=False)
#
#         response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#
#         response['Content-Disposition'] = 'attachment; filename="report_{date}.xlsx"'.format(
#             date=datetime.today().date()
#         )
#         return response

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from datetime import datetime
#from .models import PointProxyRaport
from apps.common.utils.excel_export import export


class ExportUserCosts(APIView):
    """
    Klasa widoku Django Rest Framework, która zwraca raport Excel
    (plik .xlsx) z punktami przypisanymi do zalogowanego użytkownika.
    """

    def get(self, request, format=None):
        if not request.user.is_authenticated:
            # Zwracamy 403, jeśli użytkownik nie jest zalogowany
            return Response({'detail': 'Musisz być zalogowany!'}, status=403)

        # Filtrowanie punktów na podstawie zalogowanego użytkownika
        queryset = PointProxyRaport.objects.filter(division__account=request.user)

        file_path = 'app/templates/excel_point_template.xlsx'
        print(len(queryset))
        response = export(
            request=request,
            file_path=file_path,
            file_name='costs',
            queryset=queryset,
            start_row=4,
            index_column=True,
        )

        # Ustawiamy nagłówek Content-Type na XLSX
        # (domyślnie w `export()` był 'application/ms-excel', co też często działa,
        #  ale lepszy będzie oficjalny typ MIME dla XLSX).
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # Ustawiamy nazwę pliku (z rozszerzeniem .xlsx)
        response['Content-Disposition'] = 'attachment; filename="report_{date}.xlsx"'.format(
            date=datetime.today().date()
        )

        return response



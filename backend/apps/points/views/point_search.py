import pandas as pd
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import JSONParser
from apps.points.models import Point
from apps.points.serializers import PPEFilterSerializer, PointSerializer


class PPESearchViewSet(ViewSet):
    parser_classes = [JSONParser]  # Umożliwienie odbierania JSON-a w body

    def create(self, request):
        serializer = PPEFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data

        # Filtrowanie
        queryset = Point.objects.all()
        if "ppe_number" in filters:
            queryset = queryset.filter(ppe_number__icontains=filters["ppe_number"])
        if "nip" in filters:
            queryset = queryset.filter(division__nip__icontains=filters["nip"])
        if "receiver" in filters:
            queryset = queryset.filter(division__receiver__icontains=filters["receiver"])
        if "seller" in filters:
            queryset = queryset.filter(seller__icontains=filters["seller"])
        if "tariff" in filters:
            queryset = queryset.filter(tariff__icontains=filters["tariff"])
        if "counter_number" in filters:
            queryset = queryset.filter(counter_number__icontains=filters["counter_number"])
        if "region" in filters:
            queryset = queryset.filter(city__icontains=filters["region"])
        if "osd_number" in filters:
            queryset = queryset.filter(osd_number__icontains=filters["osd_number"])

        # Sortowanie
        if "sort_by" in filters:
            queryset = queryset.order_by(filters["sort_by"])

        serialized_data = PointSerializer(queryset, many=True).data
        return Response(serialized_data)

    # @action(detail=False, methods=["post"])
    # def export_excel(self, request):
    #     serializer = PPEFilterSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     filters = serializer.validated_data
    #
    #     queryset = Point.objects.all()
    #     if "ppe_number" in filters:
    #         queryset = queryset.filter(ppe_number__icontains=filters["ppe_number"])
    #     if "nip" in filters:
    #         queryset = queryset.filter(division__nip__icontains=filters["nip"])
    #     if "receiver" in filters:
    #         queryset = queryset.filter(division__receiver__icontains=filters["receiver"])
    #     if "seller" in filters:
    #         queryset = queryset.filter(seller__icontains=filters["seller"])
    #     if "tariff" in filters:
    #         queryset = queryset.filter(tariff__icontains=filters["tariff"])
    #     if "counter_number" in filters:
    #         queryset = queryset.filter(counter_number__icontains=filters["counter_number"])
    #     if "region" in filters:
    #         queryset = queryset.filter(city__icontains=filters["region"])
    #     if "osd_number" in filters:
    #         queryset = queryset.filter(osd_number__icontains=filters["osd_number"])
    #
    #     df = pd.DataFrame.from_records(queryset.values())
    #
    #     for column in df.select_dtypes(include=["datetime64[ns, UTC]"]):
    #         df[column] = df[column].dt.tz_localize(None)
    #     response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    #     response["Content-Disposition"] = 'attachment; filename="ppe_data.xlsx"'
    #     df.to_excel(response, index=False)
    #     return response
    @action(detail=False, methods=["post"])
    def export_excel(self, request):
        serializer = PPEFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data

        # Pobranie listy dostępnych pól modelu Point
        available_columns = [field.name for field in Point._meta.fields]

        # Pobranie parametrów wyszukiwania
        queryset = Point.objects.all()
        if "ppe_number" in filters:
            queryset = queryset.filter(ppe_number__icontains=filters["ppe_number"])
        if "nip" in filters:
            queryset = queryset.filter(division__nip__icontains=filters["nip"])
        if "receiver" in filters:
            queryset = queryset.filter(division__receiver__icontains=filters["receiver"])
        if "seller" in filters:
            queryset = queryset.filter(seller__icontains=filters["seller"])
        if "tariff" in filters:
            queryset = queryset.filter(tariff__icontains=filters["tariff"])
        if "counter_number" in filters:
            queryset = queryset.filter(counter_number__icontains=filters["counter_number"])
        if "region" in filters:
            queryset = queryset.filter(city__icontains=filters["region"])
        if "osd_number" in filters:
            queryset = queryset.filter(osd_number__icontains=filters["osd_number"])

        # Konwersja do DataFrame
        df = pd.DataFrame.from_records(queryset.values())

        # Usunięcie strefy czasowej z dat
        for column in df.select_dtypes(include=["datetime64[ns, UTC]"]):
            df[column] = df[column].dt.tz_localize(None)

        # Pobranie kolumn do eksportu (jeśli podano)
        selected_columns = request.data.get("columns", available_columns)
        selected_columns = [col for col in selected_columns if
                            col in available_columns]  # Usunięcie niepoprawnych kolumn

        # Filtrowanie tylko wybranych kolumn
        df = df[selected_columns]

        # Generowanie Excela
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="ppe_data.xlsx"'
        df.to_excel(response, index=False)
        return response
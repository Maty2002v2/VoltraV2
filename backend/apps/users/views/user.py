from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
import requests

from apps.users.models.user import User
from apps.division.models.division import Division
from apps.points.models.point import Point
from ..serializers import PointSerializer, ContactDataSerializer, DivisionSerializer


OKAYCRM_API_KEY = "9ebd0453a8aba6d8d2f73a084a94f4a87477c306"
OKAYCRM_PERSONS_URL = "https://voltratest.okaycrm.com/api/v2/persons/"

class ContactDataViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Pobranie danych użytkownika (GET /api/user/contact-data/) """
        user = request.user
        contact_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.profile.phone_number if hasattr(user, "profile") else None,
            "client_number": user.profile.client_number if hasattr(user, "profile") else None,
        }
        return Response(contact_data)

    def update(self, request, pk=None):
        """ Aktualizacja danych użytkownika (PATCH /api/user/contact-data/3/) """
        try:
            user = User.objects.get(pk=pk)  # Pobieramy użytkownika z bazy
        except User.DoesNotExist:
            return Response({"error": "Użytkownik nie istnieje"}, status=404)

        serializer = ContactDataSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # 🔹 Teraz poprawnie wywołujemy aktualizację w OkayCRM
            self.update_okaycrm_person(user)

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def update_okaycrm_person(self, user):
        """ Aktualizacja danych użytkownika w OkayCRM """
        client_id = user.profile.client_number if hasattr(user, "profile") else None
        if not client_id:
            return  # Brak powiązania z OkayCRM, pomijamy

        url = f"{OKAYCRM_PERSONS_URL}{client_id}/"
        headers = {
            "Content-Type": "application/json",
            "Api-Key": OKAYCRM_API_KEY
        }

        payload = {
            "imie": user.first_name,
            "nazwisko": user.last_name,
            "email": user.email,
            "telefon": user.profile.phone_number if hasattr(user, "profile") else None,
        }

        response = requests.patch(url, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"❌ Błąd aktualizacji w OkayCRM: {response.status_code} {response.text}")
        else:
            print(f"✅ Zaktualizowano użytkownika w OkayCRM: {response.json()}")



class DivisionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Pobranie listy wszystkich działów powiązanych z użytkownikiem """
        divisions = Division.objects.all()  # Pobieramy wszystkie działy
        serializer = DivisionSerializer(divisions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ Pobranie pojedynczego Division """
        try:
            division = Division.objects.get(pk=pk)
        except Division.DoesNotExist:
            return Response({"error": "Nie znaleziono działu"}, status=404)

        serializer = DivisionSerializer(division)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """ Aktualizacja danych Division """
        try:
            division = Division.objects.get(pk=pk)
        except Division.DoesNotExist:
            return Response({"error": "Nie znaleziono działu"}, status=404)

        serializer = DivisionSerializer(division, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)




class PointViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Pobranie listy wszystkich punktów powiązanych z użytkownikiem """
        points = Point.objects.all()
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ Pobranie pojedynczego Point """
        try:
            point = Point.objects.get(pk=pk)
        except Point.DoesNotExist:
            return Response({"error": "Nie znaleziono punktu"}, status=404)

        serializer = PointSerializer(point)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """ Aktualizacja danych Point """
        try:
            point = Point.objects.get(pk=pk)
        except Point.DoesNotExist:
            return Response({"error": "Nie znaleziono punktu"}, status=404)

        serializer = PointSerializer(point, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

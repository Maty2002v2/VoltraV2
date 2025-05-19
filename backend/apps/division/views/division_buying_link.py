from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


class DivisionBuyingGroupLinkView(APIView):
    """
    Widok zwracający link do grupy zakupowej przypisanej do użytkownika.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user

        # Pobierz pierwszą jednostkę przypisaną do użytkownika
        division = user.divisions.first()
        if not division:
            raise NotFound("Użytkownik nie ma przypisanej żadnej jednostki.")

        # Pobierz pierwszą grupę zakupową przypisaną do jednostki
        buying_group = division.buying_groups.first()
        if not buying_group:
            raise NotFound("Jednostka użytkownika nie jest przypisana do żadnej grupy zakupowej.")

        # Ponieważ w BuyingGroupLink jest OneToOneField, link pobieramy bezpośrednio:
        buying_group_link = getattr(buying_group, 'link', None)
        if not buying_group_link:
            raise NotFound("Nie znaleziono linku do zakupów dla tej grupy zakupowej.")

        data = {
            "buying_group": buying_group.name,
            "link": buying_group_link.link,
        }

        return Response(data)
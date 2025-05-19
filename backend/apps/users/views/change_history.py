from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.models import UserProfile, ChangeHistory
import json

class ChangeHistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, user_id=None):
        history = ChangeHistory.objects.filter(user_id=user_id).order_by('-changed_at')
        return Response([
            {
                "field": h.field_name,
                "old_value": h.old_value,
                "new_value": h.new_value,
                "changed_at": h.changed_at
            }
            for h in history
        ])

    def restore(self, request, user_id=None, field_name=None):
        try:
            history_entry = ChangeHistory.objects.filter(user_id=user_id, field_name=field_name).order_by(
                '-changed_at').first()
            if not history_entry:
                return Response({"error": "Brak historii dla tego pola"}, status=404)

            user = UserProfile.objects.get(pk=user_id)
            setattr(user, field_name, json.loads(history_entry.old_value))
            user.save()

            return Response({"message": f"Przywrócono wartość pola {field_name}"}, status=200)
        except UserProfile.DoesNotExist:
            return Response({"error": "Użytkownik nie istnieje"}, status=404)
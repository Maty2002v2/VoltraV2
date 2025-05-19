from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from apps.files.serializers import (
    DocumentSerializer,
    DocumentCategorySerializer,
    DocumentShareSerializer,
    DocumentAccessSerializer,
    DocumentUploadSerializer)


from apps.files.models import File, Document, DocumentCategory, DocumentAccess
from apps.files.serializers import FileSerializer


class FileAPIView(object):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    authentication_classes = [authentication.JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]



class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by("-created_at")
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtruje dokumenty użytkownika + publiczne"""
        user = self.request.user
        return Document.objects.filter(models.Q(user=user) | models.Q(is_public=True))

    def perform_create(self, serializer):
        """Tworzy dokument przypisując go do użytkownika"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], url_path="share")
    def share_document(self, request, pk=None):
        """Udostępnianie dokumentu innemu użytkownikowi"""
        document = get_object_or_404(Document, pk=pk)
        if document.user != request.user:
            return Response({"error": "Nie masz uprawnień!"}, status=403)

        target_user_id = request.data.get("user_id")
        target_user = get_object_or_404(User, pk=target_user_id)

        DocumentAccess.objects.get_or_create(document=document, user=target_user, access_type="read")
        return Response({"message": "Udostępniono dokument"})
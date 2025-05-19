import os

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View


class FileDownloadView(View):
    @method_decorator(staff_member_required, name='get')
    def get(self, request, directory, filename):
        path = os.path.join(
            settings.BASE_DIR,
            'uploaded_files',
            directory,
            filename,
        )
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename={filename}'.format(filename=os.path.basename(path))
            return response
####

from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from apps.files.models import Document

class UserDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Pobiera listę dokumentów przypisanych do zalogowanego użytkownika.
        """
        user_documents = Document.objects.filter(user=request.user)
        documents_data = [
            {
                "id": doc.id,
                "name":doc.original_name,
                "description": doc.description,
            }
            for doc in user_documents
        ]
        return Response(documents_data)

class DownloadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):
        """
        Pobiera określony dokument, jeśli należy do zalogowanego użytkownika.
        """
        document = get_object_or_404(Document, id=document_id, user=request.user)
        response = FileResponse(
            document.file_content,
            content_type=document.mime_type or "application/octet-stream"
        )
        response["Content-Disposition"] = f"attachment; filename={document.original_name}"
        return response
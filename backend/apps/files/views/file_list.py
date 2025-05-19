import os

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response

from apps.files.models import File, FileType
from apps.files.serializers import FileSerializer
from apps.files.views import FileAPIView


class FileListView(FileAPIView, ListCreateAPIView):
    parser_classes = (MultiPartParser, FileUploadParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        point_id = request.data.get('point_id')
        file_type = request.data.get('file_type')
        if not point_id or not file_type:
            raise ValidationError('Missing required attributes')
        path = os.path.join(
            settings.BASE_DIR,
            'uploaded_files',
            FileType.file_path(file_type),
            file.name,
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        file = File.objects.create(location=path, file_type=file_type, point_id=point_id)
        return Response(FileSerializer(file).data, status=status.HTTP_201_CREATED)


from rest_framework.generics import RetrieveAPIView

from apps.files.views import FileAPIView


class FileDetailView(FileAPIView, RetrieveAPIView):
    pass

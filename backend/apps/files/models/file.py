from django.db import models
from django.contrib.auth.models import User

class FileType(models.IntegerChoices):
    INVOICE = 1
    AGREEMENT = 2
    COMMENTS = 3

    @staticmethod
    def file_path(file_type):
        return dict(FileType.choices).get(int(file_type), 'others').lower()


class File(models.Model):
    location = models.CharField(max_length=128, verbose_name='ścieżka')
    file_type = models.IntegerField(choices=FileType.choices, default=FileType.COMMENTS, verbose_name='typ')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    point = models.ForeignKey('points.Point', related_name='files', on_delete=models.CASCADE, verbose_name='punkt')

    class Meta(object):
        verbose_name = 'plik'
        verbose_name_plural = 'pliki'

    def __str__(self):
        return self.location
class DocumentCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    description = models.TextField(verbose_name="Opis dokumentu")
    file_content = models.BinaryField(verbose_name="Treść pliku")  # Dane binarne
    original_name = models.CharField(max_length=255, verbose_name="Oryginalna nazwa pliku")
    mime_type = models.CharField(max_length=100, verbose_name="Typ MIME", blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Użytkownik"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Data modyfikacji")

    def __str__(self):
        return f"Dokument {self.id}: {self.description[:50]}"


class Document(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(verbose_name="Opis dokumentu")
    file_content = models.BinaryField(verbose_name="Treść pliku")
    original_name = models.CharField(max_length=255, verbose_name="Oryginalna nazwa pliku")
    mime_type = models.CharField(max_length=255, verbose_name="Typ MIME", blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Użytkownik")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=False)  # Flaga publiczności

    def __str__(self):
        return f"Dokument {self.id}: {self.description[:50]}"


class DocumentAccess(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=10, choices=[("read", "Read"), ("write", "Write")])

    class Meta:
        unique_together = ("document", "user")  # Każdy użytkownik może mieć jeden wpis na dokument

    def __str__(self):
        return f"{self.user.username} - {self.document.original_name} ({self.access_type})"




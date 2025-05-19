from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.files.models import File, Document, DocumentCategory, DocumentAccess


class FileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = File
        fields = '__all__'

class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ["id", "name", "created_at", "modified_at"]

class DocumentSerializer(serializers.ModelSerializer):
    category = DocumentCategorySerializer(read_only=True)
    user = serializers.StringRelatedField()  # Zwraca `username` użytkownika

    class Meta:
        model = Document
        fields = [
            "id",
            "description",
            "original_name",
            "mime_type",
            "user",
            "category",
            "is_public",
            "created_at",
            "modified_at",
        ]


class DocumentUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)  # Obsługuje przesyłanie plików

    class Meta:
        model = Document
        fields = ["description", "file", "category", "is_public"]

    def create(self, validated_data):
        """Obsługa zapisu pliku do BinaryField"""
        file = validated_data.pop("file")
        validated_data["original_name"] = file.name
        validated_data["mime_type"] = file.content_type
        validated_data["file_content"] = file.read()  # Konwersja na BLOB

        return Document.objects.create(**validated_data)

class DocumentShareSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        """Sprawdza, czy użytkownik istnieje"""

        User = get_user_model()
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Podany użytkownik nie istnieje.")
        return value


class DocumentAccessSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Zwraca username użytkownika

    class Meta:
        model = DocumentAccess
        fields = ["id", "document", "user", "access_type"]

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms

from apps.files.models import File
from apps.files.models import Document
from django.http import HttpResponse


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'location', 'file_type', 'point', 'created_at', 'file_download',
    )
    readonly_fields = (
        'file_download',
        'created_at',
    )

    def file_download(self, obj):
        *_, directory, filename = obj.location.split('/')
        url = reverse('file_download', kwargs={'directory': directory, 'filename': filename})
        return mark_safe('<a href="{url}">DOWNLOAD</a>'.format(url=url))  # noqa: S308, S703 # nosec

from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import reverse
import zipfile
from io import BytesIO


class DocumentAdminForm(forms.ModelForm):
    uploaded_file = forms.FileField(
        label="Plik do załadowania",
        required=True,
    )

    class Meta:
        model = Document
        fields = ('description', 'user')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Zapisz zawartość pliku i metadane
        uploaded_file = self.cleaned_data.get('uploaded_file')
        if uploaded_file:
            instance.file_content = uploaded_file.read()
            instance.original_name = uploaded_file.name
            instance.mime_type = uploaded_file.content_type

        if commit:
            instance.save()
        return instance



@admin.action(description="Pobierz wybrane dokumenty jako ZIP")
def download_documents_as_zip(modeladmin, request, queryset):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for document in queryset:
            if document.file_content:
                zip_file.writestr(
                    document.original_name or f"{document.id}.bin",
                    document.file_content
                )
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="documents.zip"'
    return response



@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('id', 'description', 'user', 'download_link', 'created_at', 'modified_at')
    search_fields = ('description', 'user__username')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'modified_at')
    actions = [download_documents_as_zip]
    fieldsets = (
        (None, {
            'fields': ('description', 'uploaded_file', 'user'),
        }),
        ('Informacje systemowe', {
            'fields': ('created_at', 'modified_at'),
        }),
    )

    def download_link(self, obj):
        if obj.file_content:
            return format_html(
                '<a href="{}" target="_blank">Pobierz</a>',
                reverse('admin:download_document', args=[obj.id])
            )
        return "Brak pliku"
    download_link.short_description = "Pobierz plik"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                'download/<int:document_id>/',
                self.admin_site.admin_view(self.download_file),
                name='download_document'
            ),
        ]
        return custom_urls + urls

    def download_file(self, request, document_id):
        from django.shortcuts import get_object_or_404
        document = get_object_or_404(Document, id=document_id)

        if document.file_content:
            response = HttpResponse(document.file_content,
                                    content_type=document.mime_type or 'application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.original_name}"'
            return response
        return HttpResponse("Brak pliku", status=404)

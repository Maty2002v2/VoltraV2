from django.contrib import admin

from apps.points.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

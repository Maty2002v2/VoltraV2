from itertools import chain

from django.contrib import admin

from apps.common.utils.excel_export import export
from apps.division.models import Division
from apps.points.models import Point


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = search_fields = ('name', 'address', 'nip')  # noqa: WPS429
    list_filter = ('buying_groups',)
    actions = ['export_points']

    @admin.action(description='Wyeksportuj punkty należące do dywizji')
    def export_points(self, request, queryset):
        file_path = 'app/templates/excel_point_template.xlsx'
        points = list(chain(*[division.points.all() for division in queryset]))
        return export(request, file_path, 'points', points, Point.EXPORT_START_ROW)

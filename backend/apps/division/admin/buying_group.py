# from itertools import chain
#
# from django.contrib import admin
#
# from apps.common.utils.excel_export import export
# from apps.division.models import BuyingGroup
# from apps.points.models import Point
#
#
# @admin.register(BuyingGroup)
# class BuyingGroupAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     filter_horizontal = ('divisions',)
#     actions = ['export_points']
#
#     @admin.action(description='Wyeksportuj punkty należące do grupy zakupowej')
#     def export_points(self, request, queryset):
#         file_path = 'app/templates/excel_point_template.xlsx'
#         divisions = list(chain(*[buying_group.divisions.all() for buying_group in queryset]))
#         points = list(chain(*[division.points.all() for division in divisions]))
#         return export(request, file_path, 'points', points, Point.EXPORT_START_ROW)

from itertools import chain
from django.contrib import admin
from apps.common.utils.excel_export import export
from apps.division.models.buying_group import BuyingGroup, BuyingGroupLink
from apps.points.models import Point


class BuyingGroupLinkInline(admin.StackedInline):
    model = BuyingGroupLink
    extra = 0  # Brak pustych formularzy na zapas
    can_delete = True  # Pozwól na usuwanie istniejących linków
    verbose_name = "Link do platformy zakupowej"
    verbose_name_plural = "Linki do platform zakupowych"


@admin.register(BuyingGroup)
class BuyingGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    filter_horizontal = ('divisions',)
    actions = ['export_points']
    inlines = [BuyingGroupLinkInline]  # Dodajemy inline do zarządzania linkami

    @admin.action(description='Wyeksportuj punkty należące do grupy zakupowej')
    def export_points(self, request, queryset):
        file_path = 'app/templates/excel_point_template.xlsx'
        divisions = list(chain(*[buying_group.divisions.all() for buying_group in queryset]))
        points = list(chain(*[division.points.all() for division in divisions]))
        return export(request, file_path, 'points', points, Point.EXPORT_START_ROW)

    def link_to_platform(self, obj):
        if hasattr(obj, 'link'):  # Sprawdzamy, czy grupa ma przypisany link
            return obj.link.link  # Pobieramy link
        return "Brak linku"
    link_to_platform.short_description = "Link do platformy zakupowej"

    list_display = ('name', 'link_to_platform')
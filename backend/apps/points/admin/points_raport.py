from django.contrib import admin
from ..models import PointProxyRaport
from django.http import HttpResponse
import csv
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from apps.common.utils.excel_export import export


@admin.register(PointProxyRaport)
class PointsRaportAdmin(admin.ModelAdmin):
    list_display = ('name', 'division',)
    search_fields = ('point__name', 'division__name',)
    list_filter = ('division',)  # Dodanie opcji filtrowania po jednostce
    actions = ['export_costs']

    # Domyślna liczba wyników na stronie
    list_per_page = 100000  # Możesz ustawić domyślną wartość, np. 100

    def changelist_view(self, request, extra_context=None):
        """
        Dodanie możliwości wyświetlenia wszystkich wyników na jednej stronie.
        """
        if 'all' in request.GET:
            self.list_per_page = PointProxyRaport.objects.count()  # Wyświetl wszystkie rekordy
        return super().changelist_view(request, extra_context)

    @admin.action(description='Wyeksportuj wybrane punkty PPE')
    def export_costs(self, request, queryset):
        file_path = 'app/templates/excel_cost_template.xlsx'
        return export(request, file_path, 'costs', queryset, 1, index_column=False)
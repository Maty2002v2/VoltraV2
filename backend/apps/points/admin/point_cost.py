from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from apps.common.utils.excel_export import export
from apps.points.forms import PointsCostImportForm
from apps.points.importers import PointCostImporter
from apps.points.models import PointCost


@admin.register(PointCost)
class PointCostAdmin(admin.ModelAdmin):
    list_display = ('date', 'payer_number', 'usage', 'brutto', 'point')
    search_fields = ('point__name',)
    actions = ['export_costs']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import_costs/', self.import_costs, name='import_costs')]
        return my_urls + urls

    urls = property(get_urls)

    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        if isinstance(view, TemplateResponse):
            view.context_data['form'] = PointsCostImportForm
        return view

    @staticmethod
    def import_costs(request):
        if request.method == 'POST':
            form = PointsCostImportForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                try:
                    importer = PointCostImporter(file)
                    importer.import_costs()
                    messages.add_message(request, messages.INFO, 'Import zakończony sukcesem.')
                except Exception as error:
                    messages.add_message(request, messages.ERROR, repr(error))
        url = reverse('admin:points_pointcost_changelist')
        return HttpResponseRedirect(url)

    @admin.action(description='Wyeksportuj wybrane koszty')
    def export_costs(self, request, queryset):
        file_path = 'app/templates/excel_cost_template.xlsx'
        return export(request, file_path, 'costs', queryset, PointCost.EXPORT_START_ROW, index_column=False)

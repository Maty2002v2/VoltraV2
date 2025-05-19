from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from apps.common.utils.excel_export import export
from apps.points.forms import ConsumptionImportForm
from apps.points.importers import ConsumptionImporter
from apps.points.models.point import PointProxy


@admin.register(PointProxy)
class ConsumptionAdmin(admin.ModelAdmin):

    change_list_template = 'admin/points/change_list.html'
    list_display = ('name', 'ppe_number', 'annual_consumption')
    list_display_links = ('ppe_number','annual_consumption')
    search_fields = ('ppe_number',)
    list_filter = ('tags', 'division')
    actions = ['export_points']


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import_consumption/', self.import_consumption, name='import_consumption')]
        return my_urls + urls

    urls = property(get_urls)

    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        if isinstance(view, TemplateResponse):
            view.context_data['form'] = ConsumptionImportForm
        return view


    @staticmethod
    def import_consumption(request):
        if request.method == 'POST':
            form = ConsumptionImportForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                try:
                    importer = ConsumptionImporter(file)
                    importer.import_consumption()
                    messages.add_message(request, messages.INFO, 'Import zakończony sukcesem.')
                except Exception as error:
                    messages.add_message(request, messages.ERROR, repr(error))
        url = reverse('admin:points_pointproxy_changelist')
        return HttpResponseRedirect(url)
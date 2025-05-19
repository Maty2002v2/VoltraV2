from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from apps.common.utils.excel_export import export
from apps.points.forms import PointsImportForm
from apps.points.importers import PointImporter
from apps.points.models import Point


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    change_list_template = 'admin/points/change_list.html'
    list_display = ('name', 'ppe_number', 'address', 'division')
    list_display_links = ('name', 'ppe_number')
    search_fields = (
        'division__name',
        'city',
        'street',
        'street_number',
        'zip_code',
        'post',
        'tags__name',
    )
    list_filter = ('tags', 'division')
    actions = ['export_points']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import_points/', self.import_points, name='import_points')]
        return my_urls + urls

    urls = property(get_urls)

    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        if isinstance(view, TemplateResponse):
            view.context_data['form'] = PointsImportForm
        return view

    @staticmethod
    def import_points(request):
        if request.method == 'POST':
            form = PointsImportForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                try:
                    importer = PointImporter(file)
                    importer.import_points()
                    messages.add_message(request, messages.INFO, 'Import zakończony sukcesem.')
                except Exception as error:
                    messages.add_message(request, messages.ERROR, repr(error))
        url = reverse('admin:points_point_changelist')
        return HttpResponseRedirect(url)

    @admin.action(description='Wyeksportuj wybrane punkty')
    def export_points(self, request, queryset):
        file_path = 'app/templates/excel_point_template.xlsx'
        return export(request, file_path, 'points', queryset, Point.EXPORT_START_ROW)

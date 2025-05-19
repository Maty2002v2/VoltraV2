import django_filters

from apps.common.filters.tags import TagsFilter
from apps.division.models import Division


class DivisionFilter(TagsFilter):
    lookup_field = 'points__tags'
    costs_date = django_filters.DateFromToRangeFilter(field_name='points__costs__date', distinct=True)

    class Meta(object):
        model = Division
        fields = ()

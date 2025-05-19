from django_filters import DateFromToRangeFilter

from apps.common.filters.tags import TagsFilter
from apps.points.models import Point


class PointFilter(TagsFilter):
    lookup_field = 'tags'
    costs_date = DateFromToRangeFilter(field_name='costs__date', distinct=True)

    class Meta(object):
        model = Point
        fields = ()

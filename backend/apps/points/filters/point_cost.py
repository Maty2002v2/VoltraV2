from django_filters import DateFromToRangeFilter, FilterSet

from apps.points.models import PointCost


class PointCostFilter(FilterSet):
    costs_date = DateFromToRangeFilter(field_name='date', distinct=True)

    class Meta(object):
        model = PointCost
        fields = ()

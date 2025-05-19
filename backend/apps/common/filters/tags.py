import django_filters
from django.db.models import Q


class TagsFilter(django_filters.FilterSet):
    lookup_field = None

    tags = django_filters.Filter()
    empty_tags = django_filters.BooleanFilter()

    def filter_queryset(self, queryset):
        if not self.lookup_field:
            raise AttributeError("'TagsFilter' class has no attribute 'lookup_field'")

        filters_list = []

        conditions, queryset = self._filter(queryset)

        for condition in conditions:
            q_node = Q(**condition)
            filters_list.append(q_node)

        if filters_list:
            _filter = filters_list[0]
            for q_condition in filters_list[1:]:
                _filter = _filter | q_condition  # noqa: WPS350
        else:
            _filter = Q()

        return queryset.filter(_filter).distinct()

    def _filter(self, queryset):
        conditions = []

        for name, value in self.form.cleaned_data.items():
            if value is None:
                continue

            queryset = self._get_filter(name, value, conditions, queryset)

        return conditions, queryset

    def _get_filter(self, name, value, conditions, queryset):
        if name == 'tags':
            if value:
                values = value.split(',')
                conditions.append({f'{self.lookup_field}__id__in': values})
        elif name == 'empty_tags':
            if value:
                conditions.append({f'{self.lookup_field}': None})
            else:
                conditions.append({f'{self.lookup_field}__isnull': False})
        else:
            queryset = self.filters[name].filter(queryset, value)

        return queryset

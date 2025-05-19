import itertools

from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.division.models import Division
from apps.points.models import Point
from apps.points.serializers.point_costs import PointCostsSerializer
from apps.points.serializers.point_tags import PointTagsSerializer


class PointDetailSerializer(PointCostsSerializer, PointTagsSerializer):
    REPLACE_TEXT_KEY = 'to pole'
    POINT_NAME_VALIDATION_ERROR = 'Upewnij się, że nazwa punktu poboru i/lub numer PPE zostało wypełnione.'

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        if self.user:
            validated_data['division'] = Division.objects.filter(account__id=self.user.id).first()
        return super().create(validated_data=validated_data)

    def is_valid(self, raise_exception=False):
        if not getattr(self, 'initial_data', None):
            raise AttributeError(
                'Cannot call `.is_valid()` as no `data=` keyword argument was '
                'passed when instantiating the serializer instance.'  # noqa: C812
            )

        if not getattr(self, '_validated_data', None):
            self._validate_initial_data()

        self._validate_name_or_ppe_number()

        errors = self._format_errors(self._errors)

        if errors and raise_exception:
            self._raise_validation_error(errors)

        return not bool(self._errors)

    def _format_errors(self, errors):
        return [
            [error.replace(self.REPLACE_TEXT_KEY, self._get_field_verbose_name(field_name)) for error in field_errors]
            for field_name, field_errors in errors.items()
        ]

    def _get_field_verbose_name(self, field_name):
        return self.Meta.model._meta.get_field(field_name).verbose_name  # noqa: WPS437

    def _raise_validation_error(self, errors):
        response = ValidationError({'errors': list(itertools.chain(*errors))})
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        raise response

    def _validate_initial_data(self):
        try:
            self._validated_data = self.run_validation(self.initial_data)
            self._errors = {}
        except ValidationError as exc:
            self._validated_data = {}
            self._errors = exc.detail

    def _validate_name_or_ppe_number(self):
        if not self.initial_data['name'] and not self.initial_data['ppe_number']:
            self._errors.update({
                'name': [self.POINT_NAME_VALIDATION_ERROR],
            })

    class Meta(object):
        model = Point
        exclude = ('verified', 'division')

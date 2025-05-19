from django.conf import settings
from django.db import models

from apps.common.models.mixins import CreateUpdatedMixin


class Tag(CreateUpdatedMixin, models.Model):
    name = models.CharField(max_length=settings.MEDIUM_FIELD_LENGTH, unique=True, verbose_name='nazwa')

    class Meta(object):
        verbose_name = 'tag'
        verbose_name_plural = 'tagi'

    def __str__(self):
        return self.name

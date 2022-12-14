# Django
from django.db import models


class AlternovaModel(models.Model):
    created = models.DateTimeField(
        'Fecha de Creacion',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'Fecha de Actualizacion',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
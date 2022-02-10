from django.db import models

from taxinnovation.apps.utils.models import TIMBaseModel


class BaseRhCatalogModel(TIMBaseModel):
    created_by = models.ForeignKey(
        verbose_name='Usuario creador',
        to='users.User',
        on_delete=models.CASCADE,
        default=1,
        related_name='%(app_label)s_%(class)s_created'
    )
    modified_by = models.ForeignKey(
        verbose_name='Usuario editor',
        to='users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='%(app_label)s_%(class)s_modified'
    )

    class Meta:
        abstract = True

"""Address model."""

# Django
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from taxinnovation.apps.utils.models import TIMBaseModel


class PostalCodeCatalog(TIMBaseModel):
    """Address model.
    """
    postal_code = models.CharField(
        verbose_name='Código postal',
        max_length=5,
        validators=[MinLengthValidator(5)]
    )
    settlement = models.CharField(
        verbose_name='Colonia',
        max_length=120
    )
    municipality = models.CharField(
        verbose_name='Municipio',
        max_length=60
    )
    city = models.CharField(
        verbose_name='Ciudad',
        max_length=60,
        blank=True
    )
    settlement_type = models.CharField(
        verbose_name='Tipo de asentamiento',
        max_length=30,
        blank=True
    )
    estate = models.CharField(
        verbose_name='Estado',
        max_length=60
    )

    class Meta:
        verbose_name = 'Código postal'
        verbose_name_plural = 'Códigos postales'

    def __str__(self):
        """Return user's str representation."""
        return '{} {} {} {}'.format(self.postal_code, self.city, self.municipality, self.estate)

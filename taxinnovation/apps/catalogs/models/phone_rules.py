"""Address model."""

# Django
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from taxinnovation.apps.utils.models import TIMBaseModel
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class NirRulesCatalog(TIMBaseModel):
    """Phone nir model.
    """
    nir = models.IntegerField(
        verbose_name='NIR',
        primary_key=True,
    )
    class Meta:
        verbose_name = 'NIR'
        verbose_name_plural = 'NIRS'

    def __str__(self):
        """Return user's str representation."""
        return '{}'.format(self.nir)


class SeriesRulesCatalog(TIMBaseModel):
    """Address model.
    """
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    nir_serie = models.IntegerField(
        verbose_name='Nir_Serie',
        primary_key=True,
    )
    
    nir = models.ForeignKey(
        verbose_name='NIR',
        on_delete=models.CASCADE,
        to='catalogs.NirRulesCatalog',
    )
    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'

    def __str__(self):
        """Return user's str representation."""
        return '{} {}'.format(self.nir_serie, self.nir)


class PhoneRulesCatalog(TIMBaseModel):
    """Phone rules model.
    """
    class KindOfNet(models.TextChoices):
        FIJO = 'FI', "Telefono fijo"
        MOVIL = 'MO', "Telefono movil"

    initial_number = models.CharField(
        verbose_name='Numero inicial',
        max_length=5,
        validators=[MinLengthValidator(0)]
    )
    final_number = models.CharField(
        verbose_name='Numero final',
        max_length=5,
        validators=[MinLengthValidator(0)]
    )
    nir_serie = models.ForeignKey(
        verbose_name='Nir_Serie',
        on_delete=models.CASCADE,
        to='catalogs.SeriesRulesCatalog',
    )
    kind_of_network = models.CharField(
        verbose_name='Tipo de red',
        max_length=2,
        choices=KindOfNet.choices,
        default=KindOfNet.MOVIL
    )
    class Meta:
        verbose_name = 'Rango'
        verbose_name_plural = 'Rangos'

    def __str__(self):
        """Return user's str representation."""
        return '{} {} {}'.format(self.initial_number, self.final_number, self.nir_serie, self.kind_of_network)
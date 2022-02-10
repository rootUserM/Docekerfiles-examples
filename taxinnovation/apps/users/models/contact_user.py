from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

from taxinnovation.apps.utils.models import TIMBaseModel


class ContactUser(TIMBaseModel):
    """
    Modelo con datos de contacto del usuario.
    Pueden ser los mismos del usuario o ser distintos.
    """
    user = models.OneToOneField(
        verbose_name='Usuario',
        to='users.User',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Nombres',
        max_length=120,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Apellido paterno',
        max_length=60,
        blank=True
    )
    second_last_name = models.CharField(
        'Apellido materno',
        max_length=60,
        blank=True,
        default=''
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        blank=True
    )
    phone_number = models.CharField(
        validators=[MinLengthValidator(10), MaxLengthValidator(10)],
        max_length=10,
        blank=True
    )

    class Meta:
        verbose_name = 'Contacto de usuario'
        verbose_name_plural = 'Contactos de usuarios'

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)


class UserAddress(TIMBaseModel):
    """Tabla de direcciones de los usuarios"""
    user = models.OneToOneField(
        verbose_name='Usuario',
        to='users.User',
        on_delete=models.CASCADE,
    )
    street = models.CharField(
        verbose_name='Calle',
        help_text='Nombre de la calle',
        max_length=255,
        default=''
    )
    external_num = models.CharField(
        verbose_name='Número externo',
        help_text='Número o letras exterior',
        max_length=10,
        default='',
    )
    internal_num = models.CharField(
        verbose_name='Número interno',
        help_text='Número o letras interior',
        max_length=10,
        default='',
    )
    postal_code = models.ForeignKey(
        verbose_name='Código postal',
        to='catalogs.PostalCodeCatalog',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dirección del candidato'
        verbose_name_plural = 'Direcciones de candidatos'
        ordering = ('id',)

    def __str__(self):
        return '{}, {}'.format(self.user.name, self.street)


class ContactUserAddress(TIMBaseModel):
    """Tabla de direcciones de los contactos de usuarios"""
    user = models.OneToOneField(
        verbose_name='Usuario',
        to='users.ContactUser',
        on_delete=models.CASCADE,
    )
    street = models.CharField(
        verbose_name='Calle',
        help_text='Nombre de la calle',
        max_length=255,
        default=''
    )
    external_num = models.CharField(
        verbose_name='Número externo',
        help_text='Número o letras exterior',
        max_length=10,
        default='',
    )
    internal_num = models.CharField(
        verbose_name='Número interno',
        help_text='Número o letras interior',
        max_length=10,
        default='',
    )
    postal_code = models.ForeignKey(
        verbose_name='Código postal',
        to='catalogs.PostalCodeCatalog',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dirección del contacto'
        verbose_name_plural = 'Direcciones de contactos'
        ordering = ('id',)

    def __str__(self):
        return '{}, {}'.format(self.user.name, self.street)

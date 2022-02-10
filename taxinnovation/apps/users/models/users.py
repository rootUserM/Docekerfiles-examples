"""User model."""

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

from taxinnovation.apps.utils.models import TIMBaseModel, CustomAbstractUser

from django.utils.translation import gettext_lazy as _


class User(TIMBaseModel, CustomAbstractUser):
    """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=(
            'Indica si el registro debe ser tratado como activo.',
            'Desmarque esta opción en lugar de borrar el registro'
        )
    )
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )
    phone_number = models.CharField(
        validators=[MinLengthValidator(10), MaxLengthValidator(10)],
        max_length=10,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'last_name']

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )
    is_taxadmin = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user is an plataform admin.'
    )
    created_by = models.ForeignKey(
        verbose_name='Usuario creador',
        to='users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='%(app_label)s_%(class)s_created'
    )
    modified_by = models.ForeignKey(
        verbose_name='Usuario editor',
        to='users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='%(app_label)s_%(class)s_modified'
    )
    contract_sended = models.BooleanField(
        'contrato_enviado',
        default=False,
        help_text=(
            'Indica si el contrato a firmar ya fue enviado'
        )
    )
    contract_signed = models.BooleanField(
        'contrato_firmado',
        default=False,
        help_text=(
            'Indica si el contrato ya fue firmado'
        )
    )
    aprovado = models.BooleanField(
        'aprovado',
        default=False,
        help_text=(
            'Indica si el usuario es aprovado'
        )
    )
    token_listo = models.CharField(
        verbose_name='token_listo',
        help_text='token de listo',
        max_length=100,
        blank=True,
        null=True
    )
    url_documento = models.CharField(
        verbose_name='url_documento',
        help_text='url documento firmamex',
        max_length=200,
        blank=True,
        null=True
    )
    ticket_documento = models.CharField(
        verbose_name='ticket_documento',
        help_text='ticket documento firmamex',
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        """Return username."""
        return self.username

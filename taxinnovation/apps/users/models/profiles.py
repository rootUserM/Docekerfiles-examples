"""Profile model."""

# Django
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

# Utilities
from taxinnovation.apps.utils.models import TIMBaseModel

from django.core.files.storage import default_storage as storage

from PIL import Image


class UserProfileRole(models.Model):
    """
    UserProfileRole.
    Table with available roles.
    """
    role = models.CharField(
        verbose_name='Rol',
        unique=True,
        max_length=24,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True,
        help_text='Fecha en que el registro fue creado.'
    )
    modified_at = models.DateTimeField(
        verbose_name='Ultima modificación',
        auto_now=True,
        help_text='Última fecha en que el registro fue modificado'
    )

    class Meta:
        verbose_name = 'Rol de usuario'
        verbose_name_plural = 'Roles de usuarios'

    def __str__(self):
        """Return role."""
        return self.role


class UserProfile(TIMBaseModel):
    """Profile model.
    A profile holds a user's public data like biography, picture,
    and statistics.
    """
    class KindOfUser(models.TextChoices):
        NATURAL = 'PF', "Persona Física"
        MORAL = 'PM', "Persona Moral"

    user = models.OneToOneField(
        verbose_name='Usuario',
        to='users.User',
        on_delete=models.CASCADE
    )
    picture = models.ImageField(  # noqa DJ01
        verbose_name='Avatar',
        upload_to='users/pictures/%Y/%m/%d/',
        blank=True,
        null=True
    )
    role = models.ForeignKey(
        verbose_name='Rol de usuario',
        on_delete=models.CASCADE,
        to='users.UserProfileRole',
        default='client'
    )
    kind_of_person = models.CharField(
        verbose_name='Tipo de persona',
        max_length=2,
        choices=KindOfUser.choices,
        default=KindOfUser.NATURAL
    )
    business_name = models.CharField(
        verbose_name='Razón social',
        max_length=256,
        blank=True,
        null=True
    )
    rfc = models.CharField(
        verbose_name='RFC',
        max_length=13,
        validators=[MinLengthValidator(12), MaxLengthValidator(13)],
        blank=True,
        null=True,
        unique=True
    )
    ciec = models.CharField(
        verbose_name='CIEC',
        help_text='Contrasñea SAT',
        max_length=32,
        blank=True,
        null=True
    )
    constitutive_act = models.FileField(
        verbose_name='Acta constitutiva',
        upload_to='users/documents/constitutive_act/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    official_identification_front = models.FileField(
        verbose_name='Identificación oficial',
        upload_to='users/documents/official_identification_front/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    official_identification_back = models.FileField(
        verbose_name='Identificación oficial',
        upload_to='users/documents/official_identification_back/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    proof_of_address = models.FileField(
        verbose_name='Comprobante de domicilio',
        upload_to='users/documents/proof_of_address/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    authority_doc = models.FileField(
        verbose_name='Poderes',
        upload_to='users/documents/authority_doc/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    curp = models.FileField(
        verbose_name='CURP',
        upload_to='users/documents/curp/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    validation_video = models.FileField(
        verbose_name='Video de validación',
        upload_to='users/documents/validation_video/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    latitud = models.CharField(
        verbose_name='Latitud',
        help_text='Latitud',
        max_length=100,
        blank=True,
        null=True
    )
    longitud = models.CharField(
        verbose_name='Longitud',
        help_text='Longitud',
        max_length=100,
        blank=True,
        null=True
    )
    num_regular_issued = models.IntegerField(
        verbose_name='num_regular_issued',
        help_text='num_regular_issued',
        blank=True,
        null=True
    )
    num_crp_issued = models.IntegerField(
        verbose_name='num_crp_issued',
        help_text='num_crp_issued',
        blank=True,
        null=True
    )
    num_payroll_issued = models.IntegerField(
        verbose_name='num_payroll_issued',
        help_text='num_payroll_issued',
        blank=True,
        null=True
    )
    num_regular_received = models.IntegerField(
        verbose_name='num_regular_received',
        help_text='num_regular_received',
        blank=True,
        null=True
    )
    num_crp_received = models.IntegerField(
        verbose_name='num_crp_received',
        help_text='num_crp_received',
        blank=True,
        null=True
    )
    num_payroll_received = models.IntegerField(
        verbose_name='num_payroll_received',
        help_text='num_payroll_received',
        blank=True,
        null=True
    )
    ip_client = models.CharField(
        verbose_name='ip_client',
        help_text='ip de cliente',
        max_length=100,
        blank=True,
        null=True
    )
    rfc_id = models.IntegerField(
        verbose_name='rfc_id',
        help_text='rfc_id',
        blank=True,
        null=True
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
        help_text='url documento de firmamex',
        max_length=100,
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

    created_by = None
    modified_by = None

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save()

        try:
            img = Image.open(self.picture)
            width, height = img.size  # Get dimensions

            if width > 720 and height > 720:
                # keep ratio but shrink down
                img.thumbnail((width, height))

            # check which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                # make square by cutting off bottom
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))

            if width > 720 and height > 720:
                img.thumbnail((720, 720))

            storage_path = storage.open(self.picture.name, "wb")
            img.save(storage_path, 'png')
            storage_path.close()

        except ValueError:
            pass


class UserTemporalMedia(TIMBaseModel):
    constitutive_act = models.ImageField(
        verbose_name='Acta constitutiva',
        upload_to='users/pictures/%Y/%m/%d/',
        blank=True,
        null=True
    )
    proof_of_address = models.FileField(
        verbose_name='Comprobante de domicilio',
        upload_to='users/documents/proof_of_address/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    official_identification_front = models.FileField(
        verbose_name='INE parte frontal',
        upload_to='users/documents/official_identification_front/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    official_identification_back = models.FileField(
        verbose_name='INE parte trasera',
        upload_to='users/documents/official_identification_back/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    authority_doc = models.FileField(
        verbose_name='Poderes',
        upload_to='users/documents/authority_doc/%Y/%m/%d/',
        max_length=300,
        blank=True
    )
    validation_video = models.FileField(
        verbose_name='Video de validacion',
        upload_to='users/documents/validation_video/%Y/%m/%d/',
        max_length=300,
        blank=True,
        null=True
    )
    curp = models.FileField(
        verbose_name='CURP',
        upload_to='users/documents/curp/%Y/%m/%d/',
        max_length=300,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.proof_of_address)

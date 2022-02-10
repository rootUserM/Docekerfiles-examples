from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.postgres.fields import ArrayField


from django.utils.translation import gettext_lazy as _
from taxinnovation.apps.utils.models import TIMBaseModel
import jsonfield
from django.utils import timezone


class Facturas(TIMBaseModel):
    """Invoices model.
    Extend from Django's Abstract User
    """
    factura_id = models.CharField(
        verbose_name='factura_id',
        help_text='factura id',
        max_length=20,
        blank=True,
        null=True
    )
    receiver_rfc = models.CharField(
        verbose_name='receiver_rfc',
        help_text='receiver_rfc',
        max_length=5000,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        verbose_name='payment_method',
        help_text='payment_method',
        max_length=5000,
        blank=True,
        null=True
    )
    receiver_name = models.CharField(
        verbose_name='receiver_name',
        help_text='receiver_name',
        max_length=5000,
        blank=True,
        null=True
    )
    validation_status_short = models.CharField(
        verbose_name='validation_status_short',
        help_text='validation_status_short',
        max_length=5000,
        blank=True,
        null=True
    )
    modified_on = models.CharField(
        verbose_name='modified_on',
        help_text='modified_on',
        max_length=5000,
        blank=True,
        null=True
    )
    validation_status = models.CharField(
        verbose_name='validation_status',
        help_text='validation_status',
        max_length=5000,
        blank=True,
        null=True
    )
    total_pass_through_taxes_by_type_mxn = models.CharField(
        verbose_name='total_pass_through_taxes_by_type_mxn',
        help_text='total_pass_through_taxes_by_type_mxn',
        max_length=5000,
        blank=True,
        null=True
    )
    subtotal = models.CharField(
        verbose_name='subtotal',
        help_text='subtotal',
        max_length=5000,
        blank=True,
        null=True
    )

    exchange_rate = models.CharField(
        verbose_name='exchange_rate',
        help_text='exchange_rate',
        max_length=5000,
        blank=True,
        null=True
    )

    cfdi_type = models.CharField(
        verbose_name='cfdi_type',
        help_text='cfdi_type',
        max_length=5000,
        blank=True,
        null=True
    )

    iva = models.CharField(
        verbose_name='iva',
        help_text='iva',
        max_length=5000,
        blank=True,
        null=True
    )
    iva_rate = models.CharField(
        verbose_name='iva_rate',
        help_text='iva_rate',
        max_length=5000,
        blank=True,
        null=True
    )
    discounts = models.CharField(
        verbose_name='discounts',
        help_text='discounts',
        max_length=5000,
        blank=True,
        null=True
    )
    adjusted_subtotal = models.CharField(
        verbose_name='adjusted_subtotal',
        help_text='adjusted_subtotal',
        max_length=5000,
        blank=True,
        null=True
    )
    issuer_rfc = models.CharField(
        verbose_name='issuer_rfc',
        help_text='rfc issuer',
        max_length=20,
        blank=True,
        null=True
    )
    uuid = models.CharField(
        verbose_name='uuid',
        help_text='uuid',
        max_length=5000,
        blank=True,
        null=True
    )
    issuer_name = models.CharField(
        verbose_name='issuer_name',
        help_text='name issuer',
        max_length=5000,
        blank=True,
        null=True
    )
    total_cents = models.CharField(
        verbose_name='total_cents',
        help_text='total_cents',
        max_length=5000,
        blank=True,
        null=True
    )
    is_income = models.BooleanField(
        _('is income'),
        default=False,
        help_text=_('Indicates if the invoice is income.'),
    )

    is_payroll = models.BooleanField(
        _('is payroll'),
        default=False,
        help_text=_('Indicates if the invoice is payroll.'),
    )
    folio = models.CharField(
        verbose_name='folio',
        help_text='folio',
        max_length=5000,
        blank=True,
        null=True
    )

    issued_on = models.DateField(
        default=timezone.now,
        verbose_name='issued_on',
        help_text='issued_on',
        max_length=5000,
        blank=True,
        null=True
    )

    canceled_on = models.CharField(
        verbose_name='canceled_on',
        help_text='canceled on',
        max_length=5000,
        blank=True,
        null=True
    )

    total = models.CharField(
        verbose_name='total',
        help_text='total',
        max_length=5000,
        blank=True,
        null=True
    )
    currency = models.CharField(
        verbose_name='currency',
        help_text='currency',
        max_length=5000,
        blank=True,
        null=True
    )
    total_retained_taxes_by_type_mxn = models.CharField(
        verbose_name='total_retained_taxes_by_type_mxn',
        help_text='total_retained_taxes_by_type_mxn',
        max_length=5000,
        blank=True,
        null=True
    )
    payment_form_display = models.CharField(
        verbose_name='payment_form_display',
        help_text='payment_form_display',
        max_length=5000,
        blank=True,
        null=True
    )

    customer_id = models.CharField(
        verbose_name='customer_id',
        help_text='customer_id',
        max_length=5000,
        blank=True,
        null=True
    )
    certified_on = models.CharField(
        verbose_name='certified_on',
        help_text='certified_on',
        max_length=5000,
        blank=True,
        null=True
    )

    xml_file_ids = ArrayField(models.CharField(max_length=200), blank=True, size=1, null=True)

    pdf_file_ids = ArrayField(models.CharField(max_length=200), blank=True, size=1, null=True)

    lineitems = ArrayField(models.CharField(max_length=5000), blank=True, size=1, null=True)

    receiver_address = models.CharField(
        verbose_name='receiver_address',
        help_text='receiver_address',
        max_length=5000,
        blank=True,
        null=True
    )
    payroll_data = models.CharField(
        verbose_name='payroll_data',
        help_text='payroll_data',
        max_length=5000,
        blank=True,
        null=True
    )
    json_invoice = jsonfield.JSONField()

    users_user = models.ForeignKey(
        verbose_name='Usuario User',
        on_delete=models.CASCADE,
        to='users.User',
    )

    class Meta:
        verbose_name = 'Informacion'
        verbose_name_plural = 'Infomracion de usuarios'

    def __str__(self):
        """Return rfc issuer."""
        return self.issuer_rfc


class DireccionLegal(TIMBaseModel):
    """Informaicion model.
    Extend from Django's Abstract User
    """
    users_direccion = models.ForeignKey(
        verbose_name='Direccion User',
        on_delete=models.CASCADE,
        to='users.User',
    )
    act_eco = models.CharField(
        verbose_name='act_eco',
        help_text='actividades economicas',
        max_length=5000,
        blank=True,
        null=True
    )
    estatus_domicilio = models.CharField(
        verbose_name='estatus_domicilio',
        help_text='estatus domicilio',
        max_length=100,
        blank=True,
        null=True
    )
    estatus_cont_dom = models.CharField(
        verbose_name='estatus_cont_dom',
        help_text='estatus contribuyente domicilio',
        max_length=200,
        blank=True,
        null=True
    )
    fecha_alta_dom = models.CharField(
        verbose_name='fecha_alta_dom',
        help_text='fecha alta domicilio',
        max_length=60,
        blank=True,
        null=True
    )
    ad = models.CharField(
        verbose_name='ad',
        help_text='ad',
        max_length=100,
        blank=True,
        null=True
    )
    nomb_ent_fed = models.CharField(
        verbose_name='nomb_ent_fed',
        help_text='nombre entidad federativa',
        max_length=100,
        blank=True,
        null=True
    )
    nomb_muni_demar_terri = models.CharField(
        verbose_name='nomb_ent_fed',
        help_text='nombre entidad federativa',
        max_length=100,
        blank=True,
        null=True
    )
    nombre_localidad = models.CharField(
        verbose_name='nombre_localidad',
        help_text='nombre localidad',
        max_length=100,
        blank=True,
        null=True
    )
    nombre_colonia = models.CharField(
        verbose_name='nombre_colonia',
        help_text='nombre colonia',
        max_length=100,
        blank=True,
        null=True
    )
    nombre_vialidad = models.CharField(
        verbose_name='nombre_vialidad',
        help_text='nombre vialidad',
        max_length=100,
        blank=True,
        null=True
    )
    numero_exterior = models.CharField(
        verbose_name='numero_exterior',
        help_text='numero exterior',
        max_length=100,
        blank=True,
        null=True
    )
    numero_interior = models.CharField(
        verbose_name='numero_interior',
        help_text='numero interior',
        max_length=100,
        blank=True,
        null=True
    )
    entre_calle = models.CharField(
        verbose_name='entre_calle',
        help_text='entre calle',
        max_length=100,
        blank=True,
        null=True
    )
    y_calle = models.CharField(
        verbose_name='y_calle',
        help_text='y calle',
        max_length=100,
        blank=True,
        null=True
    )
    tipo_vialidad = models.CharField(
        verbose_name='tipo_vialidad',
        help_text='tipo vialidad',
        max_length=100,
        blank=True,
        null=True
    )
    cod_pos = models.CharField(
        verbose_name='cod_pos',
        help_text='codigo postal',
        max_length=20,
        blank=True,
        null=True
    )
    tipo_inmueble = models.CharField(
        verbose_name='tipo_inmueble',
        help_text='tipo inmueble',
        max_length=100,
        blank=True,
        null=True
    )
    tel_fijo = models.CharField(
        verbose_name='tel_fijo',
        help_text='telefono fijo',
        max_length=20,
        blank=True,
        null=True
    )
    tel_movil = models.CharField(
        verbose_name='tel_movil',
        help_text='telefono movil',
        max_length=20,
        blank=True,
        null=True
    )
    correo = models.CharField(
        verbose_name='correo',
        help_text='correo',
        max_length=50,
        blank=True,
        null=True
    )
    referencia = models.CharField(
        verbose_name='referencia',
        help_text='referencia',
        max_length=1000,
        blank=True,
        null=True
    )
    json_direccion_legal = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion legal'

    def __str__(self):
        """Return rfc issuer."""
        return self.issuer_rfc


class Lista69b(TIMBaseModel):
    """Informaicion model.
    Extend from Django's Abstract User
    """
    counterparty_rfc = models.CharField(
        verbose_name='counterparty_rfc',
        help_text='counterparty rfc',
        max_length=25,
        blank=True,
        null=True
    )
    rfc_name = models.CharField(
        verbose_name='rfc_name',
        help_text='rfc name',
        max_length=100,
        blank=True,
        null=True
    )
    state = models.CharField(
        verbose_name='state',
        help_text='state',
        max_length=80,
        blank=True,
        null=True
    )
    list_type = models.CharField(
        verbose_name='list_type',
        help_text='list type',
        max_length=80,
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name='status',
        help_text='status',
        max_length=50,
        blank=True,
        null=True
    )
    entry_date = models.CharField(
        verbose_name='entry_date',
        help_text='entry date',
        max_length=20,
        blank=True,
        null=True
    )
    folio = models.CharField(
        verbose_name='folio',
        help_text='folio',
        max_length=100,
        blank=True,
        null=True
    )
    customer_name = models.CharField(
        verbose_name='customer_name',
        help_text='customer name',
        max_length=100,
        blank=True,
        null=True
    )
    customer_rfc = models.CharField(
        verbose_name='customer_rfc',
        help_text='customer_rfc',
        max_length=25,
        blank=True,
        null=True
    )
    users_lista69b = models.ForeignKey(
        verbose_name='Usuario Lista 69b',
        on_delete=models.CASCADE,
        to='users.User',
    )

    json_69b = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Lista69b'
        verbose_name_plural = 'Lista69b'

    def __str__(self):
        """Return rfc issuer."""
        return self.counterparty_rfc


class DeclaracionesDiots(TIMBaseModel):
    """DeclaracionesDiots model.
    Extend from Django's Abstract User
    """
    users_declaracionesdiots = models.ForeignKey(
        verbose_name='User related',
        on_delete=models.CASCADE,
        to='users.User',
        blank=True,
        null=True
    )
    filing_period_id = models.CharField(
        verbose_name='filing_period_id',
        help_text='id de periodo',
        max_length=30,
        blank=True,
        null=True
    )
    period_type = models.CharField(
        verbose_name='period_type',
        help_text='period type',
        max_length=50,
        blank=True,
        null=True
    )
    period = models.CharField(
        verbose_name='period',
        help_text='period',
        max_length=20,
        blank=True,
        null=True
    )
    year = models.IntegerField(
        verbose_name='year',
        help_text='year',
        blank=True,
        null=True
    )
    total_paid_due = models.CharField(
        verbose_name='total_paid_due',
        help_text='total paid due',
        max_length=30,
        blank=True,
        null=True
    )
    filing_due_on = models.CharField(
        verbose_name='filing_due_on',
        help_text='filing due on',
        max_length=30,
        blank=True,
        null=True
    )
    diot_due_on = models.CharField(
        verbose_name='diot_due_on',
        help_text='diot due on',
        max_length=20,
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        verbose_name='payment_status',
        help_text='payment status',
        max_length=100,
        blank=True,
        null=True
    )
    period_description = models.CharField(
        verbose_name='period_description',
        help_text='period description',
        max_length=20,
        blank=True,
        null=True
    )
    period_type_description = models.CharField(
        verbose_name='period_type_description',
        help_text='period type description',
        max_length=30,
        blank=True,
        null=True
    )
    general_status = models.CharField(
        verbose_name='general_status',
        help_text='general status',
        max_length=100,
        blank=True,
        null=True
    )
    diot_general_status = models.CharField(
        verbose_name='numero_exterior',
        help_text='numero exterior',
        max_length=100,
        blank=True,
        null=True
    )
    days_to_pay = models.CharField(
        verbose_name='days_to_pay',
        help_text='days to pay',
        max_length=30,
        blank=True,
        null=True
    )
    days_to_file = models.CharField(
        verbose_name='days_to_file',
        help_text='days to file',
        max_length=30,
        blank=True,
        null=True
    )
    to_be_paid_due = models.CharField(
        verbose_name='to_be_paid_due',
        help_text='to be paid due',
        max_length=30,
        blank=True,
        null=True
    )
    compensable_due = models.CharField(
        verbose_name='compensable_due',
        help_text='compensable due',
        max_length=30,
        blank=True,
        null=True
    )
    payable_due = models.CharField(
        verbose_name='payable_due',
        help_text='payable due',
        max_length=20,
        blank=True,
        null=True
    )
    checksum = models.CharField(
        verbose_name='checksum',
        help_text='checksum',
        max_length=30,
        blank=True,
        null=True
    )
    nearest_payment_on = models.CharField(
        verbose_name='nearest_payment_on',
        help_text='nearest payment on',
        max_length=100,
        blank=True,
        null=True
    )
    last_payment_on = models.CharField(
        verbose_name='last_payment_on',
        help_text='last payment on',
        max_length=30,
        blank=True,
        null=True
    )
    last_filing_filed_on = models.CharField(
        verbose_name='last_filing_filed_on',
        help_text='last filing filed on',
        max_length=30,
        blank=True,
        null=True
    )
    days_to_file_diot = models.CharField(
        verbose_name='days_to_file_diot',
        help_text='days to file diot',
        max_length=20,
        blank=True,
        null=True
    )
    last_diot_filed_on = models.CharField(
        verbose_name='last_diot_filed_on',
        help_text='last_diot_filed_on',
        max_length=30,
        blank=True,
        null=True
    )
    expired_taxes = models.CharField(
        verbose_name='expired_taxes',
        help_text='expired taxes',
        max_length=30,
        blank=True,
        null=True
    )
    has_unkown_payment_status = models.CharField(
        verbose_name='has_unkown_payment_status',
        help_text='has unkown payment status',
        max_length=30,
        blank=True,
        null=True
    )
    period_only_description = models.CharField(
        verbose_name='period_only_description',
        help_text='period only description',
        max_length=30,
        blank=True,
        null=True
    )
    period_short_description = models.CharField(
        verbose_name='period_short_description',
        help_text='period short description',
        max_length=30,
        blank=True,
        null=True
    )
    creditable_due = models.CharField(
        verbose_name='creditable_due',
        help_text='creditable due',
        max_length=20,
        blank=True,
        null=True
    )
    taxes = models.CharField(
        verbose_name='taxes',
        help_text='taxes',
        max_length=350,
        blank=True,
        null=True
    )
    capture_line_expire_on = models.CharField(
        verbose_name='capture_line_expire_on',
        help_text='capture line expire on',
        max_length=60,
        blank=True,
        null=True
    )
    has_complementary_filings = models.CharField(
        verbose_name='has_complementary_filings',
        help_text='has complementary filings',
        max_length=60,
        blank=True,
        null=True
    )

    json_filings_diots = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Estatus DeclaracionesDiots'
        verbose_name_plural = 'Estatus DeclaracionesDiots'

    def __str__(self):
        """Return id_dec."""
        return self.id_dec


class OpinionCumplimiento(TIMBaseModel):
    """OpinionCumplimiento model.
    Extend from Django's Abstract User
    """
    fulfillment_opinion = models.CharField(
        verbose_name='fulfillment_opinion',
        help_text='fulfillment opinion',
        max_length=1000,
        blank=True,
        null=True
    )
    fulfillment_opinion_pdf_text = models.CharField(
        verbose_name='fulfillment_opinion',
        help_text='fulfillment opinion',
        max_length=500,
        blank=True,
        null=True
    )
    json_fulfillment_opinion = jsonfield.JSONField(
        verbose_name='json_fulfillment_opinion',
        help_text='json fulfillment opinion',
        max_length=None,
        blank=True,
        null=True
    )
    users_opinioncumplimiento = models.ForeignKey(
        verbose_name='Usuario Opinion de Cumplimiento',
        on_delete=models.CASCADE,
        to='users.User',
    )

    json_fulfillment_opinion = jsonfield.JSONField()

    class Meta:
        verbose_name = 'OpinionCumplimiento'
        verbose_name_plural = 'OpinionCumplimiento'

    def __str__(self):
        """Return rfc issuer."""
        return self.fulfillment_opinion


class Declaraciones(TIMBaseModel):

    users_declaraciones = models.ForeignKey(
        verbose_name='User related',
        on_delete=models.CASCADE,
        to='users.User',
    )

    rfc = models.CharField(
        verbose_name='rfc_filing',
        help_text='rfc de la declaracion',
        max_length=300,
        blank=True,
        null=True
    )

    filing_period = models.CharField(
        verbose_name='filing_period',
        help_text='id del periodo de la declaración',
        max_length=300,
        blank=True,
        null=True
    )

    filing_id = models.CharField(
        verbose_name='filing_id',
        help_text='id de la declaracion',
        max_length=300,
        blank=True,
        null=True
    )

    filed_timestamp = models.CharField(
        verbose_name='filed_timestamp',
        help_text='hora de captura formato',
        max_length=300,
        blank=True,
        null=True
    )

    operation_number = models.CharField(
        verbose_name='operation_number',
        help_text='número de operación de la declaración',
        max_length=300,
        blank=True,
        null=True
    )

    filing_type = models.CharField(
        verbose_name='filing_type',
        help_text='tipo de la declaración',
        max_length=300,
        blank=True,
        null=True
    )

    filed_on = models.CharField(
        verbose_name='filed_on',
        help_text='fecha de la presentacion de la declaración',
        max_length=300,
        blank=True,
        null=True
    )
    capture_line_expire_on = models.CharField(
        verbose_name='capture_line_expire_on',
        help_text='fecha y hora en la que expira la línea de captura',
        max_length=300,
        blank=True,
        null=True
    )
    days_to_pay = models.CharField(
        verbose_name='days_to_pay',
        help_text='cantidad de días restantes para pagar la declaración',
        max_length=300,
        blank=True,
        null=True
    )
    general_status = models.CharField(
        verbose_name='general_status',
        help_text='estatus general de la declaración',
        max_length=300,
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        verbose_name='payment_status',
        help_text='código del estatus de pago',
        max_length=300,
        blank=True,
        null=True
    )
    unknown_payment_status = models.CharField(
        verbose_name='unknown_payment_status',
        help_text='si SAT no tiene información sobre el pago',
        max_length=300,
        blank=True,
        null=True
    )
    expired_taxes = models.CharField(
        verbose_name='expired_taxes',
        help_text='id de la declaracion',
        max_length=300,
        blank=True,
        null=True
    )
    capture_line = models.CharField(
        verbose_name='capture_line',
        help_text='línea de captura de la declaración',
        max_length=300,
        blank=True,
        null=True
    )
    total_due = models.CharField(
        verbose_name='total_due',
        help_text='monto por apgar',
        max_length=300,
        blank=True,
        null=True
    )
    total_paid_due = models.CharField(
        verbose_name='filing_id',
        help_text='monto pagado',
        max_length=300,
        blank=True,
        null=True
    )
    creditable_due = models.CharField(
        verbose_name='creditable_due',
        help_text='summa de saldos a favor acreditables',
        max_length=300,
        blank=True,
        null=True
    )
    compensable_due = models.CharField(
        verbose_name='compensable_due',
        help_text='summa de de saldos a favor compensables',
        max_length=300,
        blank=True,
        null=True
    )
    checksum = models.CharField(
        verbose_name='checksum',
        help_text='Suma de verificación',
        max_length=300,
        blank=True,
        null=True
    )
    is_paid = models.CharField(
        verbose_name='is_paid',
        help_text='si la declaración fue pagada',
        max_length=300,
        blank=True,
        null=True
    )
    bank = models.CharField(
        verbose_name='bank',
        help_text='nombre del banco con el que fue efectuado el pago',
        max_length=300,
        blank=True,
        null=True
    )
    paid_on = models.CharField(
        verbose_name='paid_on',
        help_text='fecha en la que fue efectuado el pago',
        max_length=300,
        blank=True,
        null=True
    )
    payment_operation = models.CharField(
        verbose_name='payment_operation',
        help_text='id de la declaracion',
        max_length=300,
        blank=True,
        null=True
    )
    filed_filing_file = models.CharField(
        verbose_name='filed_filing_file',
        help_text='id del archivo con Hoja de Trabajo',
        max_length=300,
        blank=True,
        null=True
    )
    receipt_filing_file = models.CharField(
        verbose_name='receipt_filing_file',
        help_text='id del archivo con Acuse del Recibo',
        max_length=300,
        blank=True,
        null=True
    )
    paid_filing_file = models.CharField(
        verbose_name='paid_filing_file',
        help_text='id del archivo con Acuse de Pago',
        max_length=300,
        blank=True,
        null=True
    )
    payment_filing_file = models.CharField(
        verbose_name='payment_filing_file',
        help_text='id del archivo con Acuse del Recibo',
        max_length=300,
        blank=True,
        null=True
    )

    json_filing = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Declaraciones'
        verbose_name_plural = 'Declaraciones'

    def __str__(self):
        """Return rfc issuer."""
        return self.filing_id


class Diots(TIMBaseModel):

    users_diots = models.ForeignKey(
        verbose_name='User related',
        on_delete=models.CASCADE,
        to='users.User',
    )
    diot_id = models.CharField(
        verbose_name='diot_id',
        help_text='Id del Diot',
        max_length=300,
        blank=True,
        null=True
    )
    rfc = models.CharField(
        verbose_name='rfc',
        help_text='rfc',
        max_length=300,
        blank=True,
        null=True
    )
    model_version = models.CharField(
        verbose_name='model_version',
        help_text='',
        max_length=300,
        blank=True,
        null=True
    )
    folder = models.CharField(
        verbose_name='folder',
        help_text='folder',
        max_length=300,
        blank=True,
        null=True
    )
    diot_type = models.CharField(
        verbose_name='diot_type',
        help_text='diot_type',
        max_length=300,
        blank=True,
        null=True
    )
    filed_on = models.CharField(
        verbose_name='filed_on',
        help_text='filed_on',
        max_length=300,
        blank=True,
        null=True
    )
    accountant = models.CharField(
        verbose_name='accountant',
        help_text='accountant',
        max_length=300,
        blank=True,
        null=True
    )
    receipt = models.CharField(
        verbose_name='receipt',
        help_text='receipt',
        max_length=300,
        blank=True,
        null=True
    )
    filing_period = models.CharField(
        verbose_name='filing_period',
        help_text='filing_period',
        max_length=300,
        blank=True,
        null=True
    )

    json_diot = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Diot'
        verbose_name_plural = 'Diots'

    def __str__(self):
        """Return rfc issuer."""
        return self.diot_id


class Detalle_Declaracion_Declaracion(TIMBaseModel):
    declaracion_detalle_id = models.CharField(
        verbose_name='declaracion_detalle_id',
        help_text='declaracion detalle id',
        max_length=500,
        blank=True,
        null=True
    )
    operation_number = models.CharField(
        verbose_name='operation_number',
        help_text='name payer',
        max_length=500,
        blank=True,
        null=True
    )
    financial_statement = models.CharField(
        verbose_name='financial_statement',
        help_text='financial_statement',
        max_length=500,
        blank=True,
        null=True
    )
    rfc = models.CharField(
        verbose_name='rfc',
        help_text='rfc',
        max_length=500,
        blank=True,
        null=True
    )
    filed_timestamp = models.CharField(
        verbose_name='filed_timestamp',
        help_text='filed_timestamp',
        max_length=500,
        blank=True,
        null=True
    )
    filing_type = models.CharField(
        verbose_name='filing_type',
        help_text='filing_type',
        max_length=500,
        blank=True,
        null=True
    )
    complimentary_type = models.CharField(
        verbose_name='complimentary_type',
        help_text='complimentary_type',
        max_length=500,
        blank=True,
        null=True
    )
    filed_on = models.CharField(
        verbose_name='filed_on',
        help_text='filed_on',
        max_length=500,
        blank=True,
        null=True
    )
    capture_line_expire_on = models.CharField(
        verbose_name='capture_line_expire_on',
        help_text='capture_line_expire_on',
        max_length=500,
        blank=True,
        null=True
    )
    unknown_payment_status = models.CharField(
        verbose_name='unknown_payment_status',
        help_text='unknown_payment_status',
        max_length=500,
        blank=True,
        null=True
    )
    capture_line = models.CharField(
        verbose_name='capture_line',
        help_text='capture_line',
        max_length=500,
        blank=True,
        null=True
    )
    total_due = models.CharField(
        verbose_name='total_due',
        help_text='total_due',
        max_length=500,
        blank=True,
        null=True
    )
    total_paid_due = models.CharField(
        verbose_name='total_paid_due',
        help_text='total_paid_due',
        max_length=500,
        blank=True,
        null=True
    )
    is_paid = models.CharField(
        verbose_name='is_paid',
        help_text='is_paid',
        max_length=500,
        blank=True,
        null=True
    )
    bank = models.CharField(
        verbose_name='bank',
        help_text='bank',
        max_length=500,
        blank=True,
        null=True
    )
    paid_on = models.CharField(
        verbose_name='paid_on',
        help_text='paid_on',
        max_length=500,
        blank=True,
        null=True
    )
    payment_operation = models.CharField(
        verbose_name='payment_operation',
        help_text='payment_operation',
        max_length=500,
        blank=True,
        null=True
    )
    filed_filing_file = models.CharField(
        verbose_name='filed_filing_file',
        help_text='filed_filing_file',
        max_length=500,
        blank=True,
        null=True
    )
    receipt_filing_file = models.CharField(
        verbose_name='receipt_filing_file',
        help_text='receipt_filing_file',
        max_length=500,
        blank=True,
        null=True
    )
    paid_filing_file = models.CharField(
        verbose_name='paid_filing_file',
        help_text='paid_filing_file',
        max_length=500,
        blank=True,
        null=True
    )
    payment_filing_file = models.CharField(
        verbose_name='payment_filing_file',
        help_text='payment_filing_file',
        max_length=500,
        blank=True,
        null=True
    )
    filing_period = models.CharField(
        verbose_name='filing_period',
        help_text='filing_period',
        max_length=500,
        blank=True,
        null=True
    )
    filing_period_type = models.CharField(
        verbose_name='filing_period_type',
        help_text='filing_period_type',
        max_length=500,
        blank=True,
        null=True
    )
    filing_period_year = models.CharField(
        verbose_name='filing_period_year',
        help_text='filing_period_year',
        max_length=500,
        blank=True,
        null=True
    )
    filing_period_period = models.DateField(
        default=timezone.now,
        verbose_name='filing_period_period',
        help_text='filing_period_period',
        max_length=5000,
        blank=True,
        null=True
    )
    credit_balance_reductions = models.CharField(
        verbose_name='credit_balance_reductions',
        help_text='credit_balance_reductions',
        max_length=500,
        blank=True,
        null=True
    )
    credit_balance_originations = models.CharField(
        verbose_name='credit_balance_originations',
        help_text='credit_balance_originations',
        max_length=500,
        blank=True,
        null=True
    )
    taxes = models.CharField(
        verbose_name='taxes',
        help_text='taxes',
        max_length=500,
        blank=True,
        null=True
    )

    users_detalle_declaracion_declaracion = models.ForeignKey(
        verbose_name='Usuario Detalle Declaracion',
        on_delete=models.CASCADE,
        to='users.User',
    )
    json_filing_detail = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Detalle_Declaracion_Declaracion'
        verbose_name_plural = 'Detalle_Declaracion_Declaraciones'

    def __str__(self):
        """Return rfc issuer."""
        return self.declaracion_detalle_id

# class Detalle_Declaracion_Declaracion_Impuestos(TIMBaseModel):


class Detalle_Factura(TIMBaseModel):

    users_detalle_factura = models.ForeignKey(
        verbose_name='User related',
        on_delete=models.CASCADE,
        to='users.User',
    )
    canceled_on = models.CharField(
        verbose_name='canceled_on',
        help_text='canceled_on',
        max_length=5000,
        blank=True,
        null=True
    )
    category_id = models.CharField(
        verbose_name='category_id',
        help_text='category_id',
        max_length=5000,
        blank=True,
        null=True
    )
    currency = models.CharField(
        verbose_name='currency',
        help_text='currency',
        max_length=5000,
        blank=True,
        null=True
    )
    customer_id = models.CharField(
        verbose_name='customer_id',
        help_text='customer_id',
        max_length=5000,
        blank=True,
        null=True
    )
    customer_rfc_id = models.CharField(
        verbose_name='customer_rfc_id',
        help_text='customer_rfc_id',
        max_length=5000,
        blank=True,
        null=True
    )
    discounts = models.CharField(
        verbose_name='discounts',
        help_text='discounts',
        max_length=5000,
        blank=True,
        null=True
    )
    discounts_mxn = models.CharField(
        verbose_name='discounts_mxn',
        help_text='discounts_mxn',
        max_length=5000,
        blank=True,
        null=True
    )

    documents = ArrayField(models.CharField(max_length=10000), blank=True, size=1, null=True)

    due_on = models.CharField(
        verbose_name='due_on',
        help_text='due_on',
        max_length=5000,
        blank=True,
        null=True
    )
    folio = models.CharField(
        verbose_name='folio',
        help_text='folio',
        max_length=5000,
        blank=True,
        null=True
    )
    invoice_id = models.CharField(
        verbose_name='invoice_id',
        help_text='invoice_id',
        max_length=5000,
        blank=True,
        null=True
    )
    is_income = models.BooleanField(
        _('is income'),
        default=False,
        help_text=_('Indicates if the tax is income.'),
    )
    is_payroll = models.BooleanField(
        _('is pallroll'),
        default=False,
        help_text=_('Indicates if the tax is payroll.'),
    )
    issued_on = models.DateField(
        default=timezone.now,
        verbose_name='issued_on',
        help_text='issued_on',
        max_length=5000,
        blank=True,
        null=True
    )
    lineitems = ArrayField(models.CharField(max_length=5000), blank=True, size=1, null=True)
    issuer_rfc = models.CharField(
        verbose_name='issuer_rfc',
        help_text='issuer_rfc',
        max_length=5000,
        blank=True,
        null=True
    )
    modified_on = models.CharField(
        verbose_name='modified_on',
        help_text='modified_on',
        max_length=5000,
        blank=True,
        null=True
    )
    payer_rfc = models.CharField(
        verbose_name='payer_rfc',
        help_text='payer_rfc',
        max_length=5000,
        blank=True,
        null=True
    )
    payroll_data_display = models.CharField(
        verbose_name='payroll_data_display',
        help_text='payroll_data_display',
        max_length=5000,
        blank=True,
        null=True
    )
    subtotal = models.CharField(
        verbose_name='subtotal',
        help_text='subtotal',
        max_length=5000,
        blank=True,
        null=True
    )
    subtotal_mxn = models.CharField(
        verbose_name='subtotal_mxn',
        help_text='subtotal_mxn',
        max_length=5000,
        blank=True,
        null=True
    )

    taxes = ArrayField(models.CharField(max_length=5000), blank=True, size=1, null=True)

    total = models.CharField(
        verbose_name='total',
        help_text='total',
        max_length=5000,
        blank=True,
        null=True
    )
    total_mxn = models.CharField(
        verbose_name='total_mxn',
        help_text='total_mxn',
        max_length=5000,
        blank=True,
        null=True
    )
    total_paid = models.CharField(
        verbose_name='total_paid',
        help_text='total_paid',
        max_length=5000,
        blank=True,
        null=True
    )
    total_paid_mxn = models.CharField(
        verbose_name='total_paid_mxn',
        help_text='total_paid_mxn',
        max_length=5000,
        blank=True,
        null=True
    )
    total_supplier_paid = models.CharField(
        verbose_name='total_supplier_paid',
        help_text='total_supplier_paid',
        max_length=5000,
        blank=True,
        null=True
    )
    total_supplier_paid_mxn = models.CharField(
        verbose_name='total_supplier_paid_mxn',
        help_text='total_supplier_paid_mxn',
        max_length=5000,
        blank=True,
        null=True
    )
    uuid = models.CharField(
        verbose_name='uuid',
        help_text='uuid',
        max_length=5000,
        blank=True,
        null=True
    )

    cancellation_receipt_id = models.CharField(
        verbose_name='cancellation_receipt_id',
        help_text='cancellation_receipt_id',
        max_length=5000,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        verbose_name='payment_method',
        help_text='payment_method',
        max_length=5000,
        blank=True,
        null=True
    )
    issuer_regime = models.CharField(
        verbose_name='issuer_regime',
        help_text='issuer_regime',
        max_length=5000,
        blank=True,
        null=True
    )
    intended_use = models.CharField(
        verbose_name='intended_use',
        help_text='intended_use',
        max_length=5000,
        blank=True,
        null=True
    )

    json_invoice_detail = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Detalle_Factura'
        verbose_name_plural = 'Detalle_Facturas'

    def __str__(self):
        """Return rfc issuer."""
        return self.tax_id

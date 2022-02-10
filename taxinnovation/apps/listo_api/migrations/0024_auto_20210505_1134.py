# Generated by Django 3.1.1 on 2021-05-05 16:34

import django.contrib.postgres.fields
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listo_api', '0023_auto_20210503_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_factura',
            name='adjusted_subtotal_mxn',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='approval_num',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='approval_year',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='approved_rejected_on',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='category_description',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='cfdi_signature',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='comments_approval_rejection',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='comments_for_supplier',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='counterparty_name',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='email_status',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='extra_header_fields',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='generated_invoice_id',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='goods_receipts',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='intended_use_display',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='issued_at',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='issued_on_display',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='issuer_address',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='issuer_name',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='issuer_regime_display',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='paid_on',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payer_address',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payer_name',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payment_acct_num',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payment_form',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payment_form_display',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payment_method_display',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payment_state',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payment_terms',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='payments',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='purchase_orders',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='supplier_paid_on',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='tax_id',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='taxes_amount',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='taxes_amount_mxn',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='taxes_tax_rate',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='taxes_tax_type',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='taxes_treatment',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='validation_status_code',
        ),
        migrations.RemoveField(
            model_name='detalle_factura',
            name='validation_status_message',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='issuer_regime_display',
        ),
        migrations.AddField(
            model_name='detalle_factura',
            name='invoice_id',
            field=models.CharField(blank=True, help_text='invoice_id', max_length=5000, null=True, verbose_name='invoice_id'),
        ),
        migrations.AddField(
            model_name='detalle_factura',
            name='json_invoice_detail',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='detalle_factura',
            name='lineitems',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5000), blank=True, null=True, size=1),
        ),
        migrations.AddField(
            model_name='detalle_factura',
            name='taxes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5000), blank=True, null=True, size=1),
        ),
        migrations.AlterField(
            model_name='detalle_factura',
            name='documents',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10000), blank=True, null=True, size=1),
        ),
    ]
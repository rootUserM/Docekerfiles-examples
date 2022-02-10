# Generated by Django 3.1.1 on 2021-05-03 19:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listo_api', '0021_auto_20210423_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='adjusted_subtotal_mxn',
            field=models.CharField(blank=True, help_text='adjusted_subtotal_mxn', max_length=5000, null=True, verbose_name='adjusted_subtotal_mxn'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='certified_on',
            field=models.CharField(blank=True, help_text='certified_on', max_length=5000, null=True, verbose_name='certified_on'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='cfdi_type',
            field=models.CharField(blank=True, help_text='cfdi_type', max_length=300, null=True, verbose_name='cfdi_type'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='customer_id',
            field=models.CharField(blank=True, help_text='customer_id', max_length=5000, null=True, verbose_name='customer_id'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='exchange_rate',
            field=models.CharField(blank=True, help_text='exchange_rate', max_length=300, null=True, verbose_name='exchange_rate'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='folio',
            field=models.CharField(blank=True, help_text='folio', max_length=300, null=True, verbose_name='folio'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='issued_on',
            field=models.CharField(blank=True, help_text='issued_on', max_length=5000, null=True, verbose_name='issued_on'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='iva_rate',
            field=models.CharField(blank=True, help_text='iva_rate', max_length=300, null=True, verbose_name='iva_rate'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='lineitems',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5000), blank=True, null=True, size=1),
        ),
        migrations.AddField(
            model_name='facturas',
            name='modified_on',
            field=models.CharField(blank=True, help_text='modified_on', max_length=5000, null=True, verbose_name='modified_on'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='payment_method',
            field=models.CharField(blank=True, help_text='payment_method', max_length=300, null=True, verbose_name='payment_method'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='payroll_data',
            field=models.CharField(blank=True, help_text='payroll_data', max_length=300, null=True, verbose_name='payroll_data'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='pdf_file_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=1),
        ),
        migrations.AddField(
            model_name='facturas',
            name='total_pass_through_taxes_by_type_mxn',
            field=models.CharField(blank=True, help_text='total_pass_through_taxes_by_type_mxn', max_length=300, null=True, verbose_name='total_pass_through_taxes_by_type_mxn'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='uuid',
            field=models.CharField(blank=True, help_text='uuid', max_length=5000, null=True, verbose_name='uuid'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='validation_status_short',
            field=models.CharField(blank=True, help_text='validation_status_short', max_length=300, null=True, verbose_name='validation_status_short'),
        ),
        migrations.AddField(
            model_name='facturas',
            name='xml_file_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=1),
        ),
        migrations.AlterField(
            model_name='lista69b',
            name='customer_rfc',
            field=models.CharField(blank=True, help_text='customer_rfc', max_length=25, null=True, verbose_name='customer_rfc'),
        ),
    ]

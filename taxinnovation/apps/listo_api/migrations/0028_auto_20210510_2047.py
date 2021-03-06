# Generated by Django 3.1.1 on 2021-05-11 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listo_api', '0027_auto_20210510_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccionlegal',
            name='act_eco',
            field=models.CharField(blank=True, help_text='actividades economicas', max_length=5000, null=True, verbose_name='act_eco'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='canceled_on',
            field=models.CharField(blank=True, help_text='canceled on', max_length=5000, null=True, verbose_name='canceled_on'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='cfdi_type',
            field=models.CharField(blank=True, help_text='cfdi_type', max_length=5000, null=True, verbose_name='cfdi_type'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='currency',
            field=models.CharField(blank=True, help_text='currency', max_length=5000, null=True, verbose_name='currency'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='exchange_rate',
            field=models.CharField(blank=True, help_text='exchange_rate', max_length=5000, null=True, verbose_name='exchange_rate'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='folio',
            field=models.CharField(blank=True, help_text='folio', max_length=5000, null=True, verbose_name='folio'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='issuer_name',
            field=models.CharField(blank=True, help_text='name issuer', max_length=5000, null=True, verbose_name='issuer_name'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='iva',
            field=models.CharField(blank=True, help_text='iva', max_length=5000, null=True, verbose_name='iva'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='iva_rate',
            field=models.CharField(blank=True, help_text='iva_rate', max_length=5000, null=True, verbose_name='iva_rate'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='payment_form_display',
            field=models.CharField(blank=True, help_text='payment_form_display', max_length=5000, null=True, verbose_name='payment_form_display'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='payment_method',
            field=models.CharField(blank=True, help_text='payment_method', max_length=5000, null=True, verbose_name='payment_method'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='payroll_data',
            field=models.CharField(blank=True, help_text='payroll_data', max_length=5000, null=True, verbose_name='payroll_data'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='receiver_address',
            field=models.CharField(blank=True, help_text='receiver_address', max_length=5000, null=True, verbose_name='receiver_address'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='receiver_name',
            field=models.CharField(blank=True, help_text='receiver_name', max_length=5000, null=True, verbose_name='receiver_name'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='receiver_rfc',
            field=models.CharField(blank=True, help_text='receiver_rfc', max_length=5000, null=True, verbose_name='receiver_rfc'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='subtotal',
            field=models.CharField(blank=True, help_text='subtotal', max_length=5000, null=True, verbose_name='subtotal'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='total',
            field=models.CharField(blank=True, help_text='total', max_length=5000, null=True, verbose_name='total'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='total_cents',
            field=models.CharField(blank=True, help_text='total_cents', max_length=5000, null=True, verbose_name='total_cents'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='total_pass_through_taxes_by_type_mxn',
            field=models.CharField(blank=True, help_text='total_pass_through_taxes_by_type_mxn', max_length=5000, null=True, verbose_name='total_pass_through_taxes_by_type_mxn'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='total_retained_taxes_by_type_mxn',
            field=models.CharField(blank=True, help_text='total_retained_taxes_by_type_mxn', max_length=5000, null=True, verbose_name='total_retained_taxes_by_type_mxn'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='validation_status',
            field=models.CharField(blank=True, help_text='validation_status', max_length=5000, null=True, verbose_name='validation_status'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='validation_status_short',
            field=models.CharField(blank=True, help_text='validation_status_short', max_length=5000, null=True, verbose_name='validation_status_short'),
        ),
    ]

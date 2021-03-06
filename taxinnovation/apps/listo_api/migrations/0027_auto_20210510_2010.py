# Generated by Django 3.1.1 on 2021-05-11 01:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listo_api', '0026_auto_20210507_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_factura',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='issued_on', max_length=5000, null=True, verbose_name='issued_on'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='issued_on', max_length=5000, null=True, verbose_name='issued_on'),
        ),
    ]

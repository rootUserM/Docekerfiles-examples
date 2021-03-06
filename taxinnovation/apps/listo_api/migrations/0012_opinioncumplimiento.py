# Generated by Django 3.1.1 on 2021-04-16 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listo_api', '0011_informacion_canceled_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpinionCumplimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text=('Indica si el registro debe ser tratado como activo.', 'Desmarque esta opción en lugar de borrar el registro'), verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Fecha en que el registro fue creado.', verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Última fecha en que el registro fue modificado', verbose_name='Ultima modificación')),
                ('fulfillment_opinion', models.CharField(blank=True, help_text='fulfillment opinion', max_length=1000, null=True, verbose_name='fulfillment_opinion')),
                ('fulfillment_opinion_pdf_text', models.CharField(blank=True, help_text='fulfillment opinion', max_length=500, null=True, verbose_name='fulfillment_opinion')),
                ('json_fulfillment_opinion', jsonfield.fields.JSONField(blank=True, help_text='json fulfillment opinion', null=True, verbose_name='json_fulfillment_opinion')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listo_api_opinioncumplimiento_created', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listo_api_opinioncumplimiento_modified', to=settings.AUTH_USER_MODEL, verbose_name='Usuario editor')),
                ('users_opinion_cumplimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Opinion de Cumplimiento')),
            ],
            options={
                'verbose_name': 'OpinionCumplimiento',
                'verbose_name_plural': 'OpinionCumplimiento',
            },
        ),
    ]

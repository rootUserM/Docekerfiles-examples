# Generated by Django 3.0.8 on 2020-08-17 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200813_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTemporalMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text=('Indica si el registro debe ser tratado como activo.', 'Desmarque esta opción en lugar de borrar el registro'), verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Fecha en que el registro fue creado.', verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Última fecha en que el registro fue modificado', verbose_name='Ultima modificación')),
                ('constitutive_act', models.ImageField(blank=True, null=True, upload_to='users/pictures/%Y/%m/%d/', verbose_name='Acta constitutiva')),
                ('proof_of_address', models.FileField(blank=True, max_length=300, upload_to='users/documents/proof_of_address/%Y/%m/%d/', verbose_name='Comprobante de domicilio')),
                ('official_identification_front', models.FileField(blank=True, max_length=300, upload_to='users/documents/official_identification_front/%Y/%m/%d/', verbose_name='INE parte frontal')),
                ('official_identification_back', models.FileField(blank=True, max_length=300, upload_to='users/documents/official_identification_back/%Y/%m/%d/', verbose_name='INE parte trasera')),
                ('authority_doc', models.FileField(blank=True, max_length=300, upload_to='users/documents/authority_doc/%Y/%m/%d/', verbose_name='Poderes')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users_usertemporalmedia_created', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_usertemporalmedia_modified', to=settings.AUTH_USER_MODEL, verbose_name='Usuario editor')),
            ],
            options={
                'ordering': ['-created_at', '-modified_at'],
                'abstract': False,
            },
        ),
    ]
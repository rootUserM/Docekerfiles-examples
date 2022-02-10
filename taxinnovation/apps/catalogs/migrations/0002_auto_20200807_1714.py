# Generated by Django 3.0.8 on 2020-08-07 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postalcodecatalog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Fecha en que el registro fue creado.', verbose_name='Fecha de creación'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postalcodecatalog',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='catalogs_postalcodecatalog_created', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador'),
        ),
        migrations.AddField(
            model_name='postalcodecatalog',
            name='is_active',
            field=models.BooleanField(default=True, help_text=('Indica si el registro debe ser tratado como activo.', 'Desmarque esta opción en lugar de borrar el registro'), verbose_name='active'),
        ),
        migrations.AddField(
            model_name='postalcodecatalog',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, help_text='Última fecha en que el registro fue modificado', verbose_name='Ultima modificación'),
        ),
        migrations.AddField(
            model_name='postalcodecatalog',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='catalogs_postalcodecatalog_modified', to=settings.AUTH_USER_MODEL, verbose_name='Usuario editor'),
        ),
    ]

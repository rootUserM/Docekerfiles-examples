# Generated by Django 3.1.2 on 2021-01-11 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_userprofile_token_listo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='latitud',
            field=models.CharField(blank=True, help_text='Latitud', max_length=100, null=True, verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='longitud',
            field=models.CharField(blank=True, help_text='Longitud', max_length=100, null=True, verbose_name='Longitud'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-08-08 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200807_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='curp',
            field=models.FileField(blank=True, max_length=300, upload_to='users/documents/curp/%Y/%m/%d/', verbose_name='CURP'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='official_identification',
            field=models.FileField(blank=True, max_length=300, upload_to='users/documents/official_identification/%Y/%m/%d/', verbose_name='Identificación oficial'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='proof_of_address',
            field=models.FileField(blank=True, max_length=300, upload_to='users/documents/proof_of_address/%Y/%m/%d/', verbose_name='Comprobante de domicilio'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='validation_video',
            field=models.FileField(blank=True, max_length=300, upload_to='users/documents/validation_video/%Y/%m/%d/', verbose_name='Video de validación'),
        ),
    ]
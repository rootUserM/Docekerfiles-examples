# Generated by Django 3.0.8 on 2020-08-28 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_usertemporalmedia_validation_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertemporalmedia',
            name='curp',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to='users/documents/curp/%Y/%m/%d/', verbose_name='CURP'),
        ),
    ]

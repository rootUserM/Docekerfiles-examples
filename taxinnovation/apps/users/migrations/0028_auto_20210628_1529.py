# Generated by Django 3.1.1 on 2021-06-28 20:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_auto_20210518_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_taxadmin',
            field=models.BooleanField(default=False, help_text='Set to true when the user is an plataform admin.', verbose_name='verified'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='rfc',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.MaxLengthValidator(13)], verbose_name='RFC'),
        ),
    ]

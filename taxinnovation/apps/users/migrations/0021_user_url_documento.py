# Generated by Django 3.1.2 on 2021-01-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20210111_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='url_documento',
            field=models.CharField(blank=True, help_text='url documento firmamex', max_length=200, null=True, verbose_name='url_documento'),
        ),
    ]

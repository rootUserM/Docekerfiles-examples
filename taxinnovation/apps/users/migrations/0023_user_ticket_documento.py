# Generated by Django 3.1.2 on 2021-01-15 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_userprofile_url_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ticket_documento',
            field=models.CharField(blank=True, help_text='ticket documento firmamex', max_length=200, null=True, verbose_name='ticket_documento'),
        ),
    ]

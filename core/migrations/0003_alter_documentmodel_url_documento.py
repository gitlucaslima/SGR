# Generated by Django 4.0.6 on 2022-09-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_documentmodel_url_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentmodel',
            name='url_documento',
            field=models.FileField(upload_to='relatorios/'),
        ),
    ]

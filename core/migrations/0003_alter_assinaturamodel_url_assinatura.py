# Generated by Django 4.0.6 on 2022-07-31 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_disciplinamodel_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assinaturamodel',
            name='url_assinatura',
            field=models.FileField(max_length=200, upload_to=''),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0005_alter_mysite_torrents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitestatus',
            name='seed_volume',
            field=models.BigIntegerField(default=0, verbose_name='做种体积'),
        ),
    ]

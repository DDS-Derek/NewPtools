# Generated by Django 4.2.1 on 2023-09-16 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0009_alter_torrentinfo_imdb_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrentinfo',
            name='pushed',
            field=models.BooleanField(default=False, help_text='推送至辅种服务器', verbose_name='推送至服务器'),
        ),
    ]

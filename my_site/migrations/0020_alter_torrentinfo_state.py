# Generated by Django 4.2.1 on 2023-05-19 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0019_alter_torrentinfo_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrentinfo',
            name='state',
            field=models.IntegerField(default=0, verbose_name='推送状态'),
        ),
    ]

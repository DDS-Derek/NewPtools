# Generated by Django 4.1.7 on 2023-05-04 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0013_mysite_remove_torrent_rules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrentinfo',
            name='sale_expire',
            field=models.CharField(default='', max_length=24, verbose_name='到期时间'),
        ),
        migrations.AlterField(
            model_name='torrentinfo',
            name='sale_status',
            field=models.CharField(default='', max_length=16, verbose_name='优惠状态'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-05-08 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_website_tracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='func_brush_flow',
            field=models.BooleanField(default=False, verbose_name='RSS刷流'),
        ),
        migrations.AlterField(
            model_name='website',
            name='func_get_torrents',
            field=models.BooleanField(default=True, verbose_name='Free刷流'),
        ),
    ]
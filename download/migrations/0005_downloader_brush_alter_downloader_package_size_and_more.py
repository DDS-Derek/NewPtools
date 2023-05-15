# Generated by Django 4.2.1 on 2023-05-15 16:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("download", "0004_downloader_count_torrents_downloader_http"),
    ]

    operations = [
        migrations.AddField(
            model_name="downloader",
            name="brush",
            field=models.BooleanField(
                default=False, help_text="刷流和保种一定要分开！", verbose_name="刷流专用"
            ),
        ),
        migrations.AlterField(
            model_name="downloader",
            name="package_size",
            field=models.IntegerField(
                default=5, help_text="单位：GB，大于这个体积才拆包", verbose_name="种子大小"
            ),
        ),
        migrations.AlterField(
            model_name="downloader",
            name="reserved_space",
            field=models.IntegerField(
                default=30,
                help_text="单位：GB，最小为1G",
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="预留磁盘空间",
            ),
        ),
    ]
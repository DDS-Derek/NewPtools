# Generated by Django 4.2.1 on 2023-06-01 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_site", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="torrentinfo",
            name="size",
            field=models.BigIntegerField(default=0, verbose_name="文件大小"),
        ),
    ]

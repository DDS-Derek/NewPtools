# Generated by Django 4.2.1 on 2023-05-19 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0018_rename_hr_mysite_hr_discern_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrentinfo',
            name='state',
            field=models.IntegerField(choices=[('未推送', 0), ('已推送', 1), ('免费过期', 2), ('已删种', 3), ('已删除', 4), ('已归档', 5)], default=0, verbose_name='推送状态'),
        ),
    ]
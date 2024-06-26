# Generated by Django 4.2.1 on 2023-05-29 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaiduOCR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(default='百度OCR', editable=False, max_length=64, unique=True, verbose_name='OCR')),
                ('enable', models.BooleanField(default=False, verbose_name='启用')),
                ('api_key', models.CharField(blank=True, max_length=64, null=True, verbose_name='API-Key')),
                ('secret_key', models.CharField(blank=True, help_text='应用的Secret', max_length=64, null=True, verbose_name='Secret')),
                ('app_id', models.CharField(blank=True, help_text='APP ID', max_length=64, null=True, verbose_name='应用ID')),
            ],
            options={
                'verbose_name': '百度OCR',
                'verbose_name_plural': '百度OCR',
            },
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(choices=[('wechat_work_push', '企业微信通知'), ('wxpusher_push', 'WxPusher通知'), ('pushdeer_push', 'PushDeer通知'), ('bark_push', 'Bark通知'), ('iyuu_push', '爱语飞飞')], default='wechat_work_push', max_length=64, unique=True, verbose_name='通知方式')),
                ('enable', models.BooleanField(default=True, help_text='只有开启才能发送哦！', verbose_name='开启通知')),
                ('corpid', models.CharField(blank=True, help_text='微信企业ID', max_length=64, null=True, verbose_name='企业ID')),
                ('corpsecret', models.CharField(blank=True, help_text='应用的Secret/Token', max_length=64, null=True, verbose_name='Secret')),
                ('agentid', models.CharField(blank=True, help_text='APP ID', max_length=64, null=True, verbose_name='应用ID')),
                ('touser', models.CharField(blank=True, help_text='接收者用户名/UID', max_length=64, null=True, verbose_name='接收者')),
                ('custom_server', models.URLField(blank=True, help_text='IYuu与BARK请必填，详情参考教程！', null=True, verbose_name='服务器')),
            ],
            options={
                'verbose_name': '通知推送',
                'verbose_name_plural': '通知推送',
            },
        ),
    ]

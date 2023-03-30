from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from auxiliary.base import BaseEntity, DownloaderCategory


# Create your models here.
class Downloader(BaseEntity):
    # 下载器名称
    name = models.CharField(max_length=12, verbose_name='名称')
    # 下载器类别             tr  qb  de
    category = models.CharField(max_length=128, choices=DownloaderCategory.choices,
                                default=DownloaderCategory.qBittorrent,
                                verbose_name='下载器')
    # 用户名
    username = models.CharField(max_length=16, verbose_name='用户名')
    # 密码
    password = models.CharField(max_length=128, verbose_name='密码')
    # 开启
    enable = models.BooleanField(default=True, verbose_name='开启')
    # host
    host = models.CharField(max_length=32, verbose_name='HOST')
    # port
    port = models.IntegerField(default=8999, verbose_name='端口', validators=[
        MaxValueValidator(65535),
        MinValueValidator(1001)
    ])
    # 预留空间
    reserved_space = models.IntegerField(default=30, verbose_name='预留磁盘空间', validators=[
        MinValueValidator(1),
        MaxValueValidator(512)
    ], help_text='单位GB，最小为1G，最大512G')

    class Meta:
        verbose_name = '下载器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

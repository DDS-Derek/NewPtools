from django.db import models


class BaseEntity(models.Model):
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True


class DownloaderCategory(models.TextChoices):
    # 下载器名称
    # Deluge = 'De', 'Deluge'
    Transmission = 'Tr', 'Transmission'
    qBittorrent = 'Qb', 'qBittorrent'

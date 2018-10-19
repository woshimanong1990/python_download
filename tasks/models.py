# coding:utf-8

import uuid

from django.db import models

from .variables import STATUS_CHOICES


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=1, default="1", verbose_name="状态", choices=)
    url = models.CharField(max_length=500, verbose_name="下载链接", default="")
    headers = models.CharField(max_length=1000, default="{}", verbose_name="请求头")
    file_size = models.IntegerField(default=0, verbose_name="文件大小")
    file_save_path = models.CharField(max_length=500, verbose_name="文件本地保存")
    connection_number = models.IntegerField(default=64, verbose_name="下载连接数")
    last_statistics_time = models.TimeField(verbose_name="上次统计时间")
    last_download_total_size = models.IntegerField(default=0, verbose_name="上次下载总量")
    current_speed = models.CharField(max_length=100, verbose_name="实时速度")

    create_time = models.DateTimeField(auto_to_add=True)
    update_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return "id:{}，url:{}".format(self.id, self.url)

    def __repr__(self):
        return "id:{}，url:{}".format(self.id, self.url)

    class Meta:
        ordering = ["-create_time"]


class TaskProgress(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_position = models.BigIntegerField(default=0, verbose_name="起始位置")
    current_position = models.BigIntegerField(default=0, verbose_name="当前位置")
    end_position = models.BigIntegerField(default=0, verbose_name="结束位置")
    total_length = models.BigIntegerField(default=0, verbose_name="段长")

    create_time = models.DateTimeField(auto_to_add=True)
    update_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)









# -*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.

# 工单
class PatrolTemplate(models.Model):
    name = models.CharField(max_length = 255)
    biz_id = models.CharField(max_length = 255)
    biz_name = models.CharField(max_length = 255)
    content = models.CharField(max_length = 500)
    domain = models.CharField(max_length = 255)
    mark = models.CharField(max_length=500)
    create_user = models.CharField(max_length = 255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField( blank=True, null=True)

    def transfer(self):
        dic = {}
        dic['id'] = self.id
        dic['name'] = self.name
        dic['biz_id'] = self.biz_id
        dic['biz_name'] = self.biz_name
        dic['content'] = self.content
        dic['domain'] = self.domain
        dic['mark'] = self.mark
        dic['create_user'] = self.create_user
        dic['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['update_time'] = self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        return dic


# 工单
class PatrolTask(models.Model):
    biz_id = models.CharField(max_length = 255)
    biz_name = models.CharField(max_length = 255)
    task_name = models.CharField(max_length=255)
    template_id = models.CharField(max_length=500)
    template_name = models.CharField(max_length = 500)
    type = models.CharField(max_length=500)
    ip = models.CharField(max_length = 255)
    create_user = models.CharField(max_length = 255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField( blank=True, null=True)

    def transfer(self):
        dic = {}
        dic['id'] = self.id
        dic['biz_id'] = self.biz_id
        dic['biz_name'] = self.biz_name
        dic['task_name'] = self.task_name
        dic['template_id'] = self.template_id
        dic['template_name'] = self.template_name
        dic['type'] = self.type
        dic['ip'] = self.ip
        dic['create_user'] = self.create_user
        dic['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['update_time'] = self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        return dic
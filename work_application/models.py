# -*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.

# 工单
class Work(models.Model):
    title = models.CharField(max_length = 255)
    approver = models.CharField(max_length=255)
    biz_id = models.CharField(max_length = 255)
    biz_name = models.CharField(max_length = 255)
    ip = models.CharField(max_length = 500)
    content = models.CharField(max_length = 500)
    status = models.CharField(max_length = 255)
    create_user = models.CharField(max_length = 255)
    create_time = models.DateTimeField()
    update_user = models.CharField(max_length = 255, default = None, blank=True, null=True)
    update_time = models.DateTimeField( blank=True, null=True)
    rejection = models.CharField(max_length = 500)
    def of(self, dict):
        self.title = dict['title']
        self.approver = dict['approver']
        self.biz_id = dict['biz_id']
        self.biz_name = dict['biz_name']
        self.ip = dict['ip']
        self.content = dict['content']
        self.status = dict['status']
        self.create_user = dict['create_user']
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()

    def transfer(self):
        dic = {}
        dic['id'] = self.id
        dic['title'] = self.title
        dic['approver'] = self.approver
        dic['biz_id'] = self.biz_id
        dic['biz_name'] = self.biz_name
        dic['ip'] = self.ip
        dic['content'] = self.content
        dic['status'] = self.status
        dic['create_user'] = self.create_user
        dic['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['update_user'] = self.update_user
        dic['update_time'] = self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['rejection'] = self.rejection
        return dic


# -*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.

# 考试
class Test(models.Model):
    biz_id = models.CharField(max_length=255)
    biz_name = models.CharField(max_length=255)
    name = models.CharField(max_length = 255)
    type = models.CharField(max_length=255)
    res = models.CharField(max_length=255)
    phone = models.CharField(max_length = 500)
    test_date = models.DateTimeField()
    addr = models.CharField(max_length = 255)
    test_title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    create_user = models.CharField(max_length = 255)
    create_time = models.DateTimeField()
    update_user = models.CharField(max_length = 255, default = None, blank=True, null=True)
    update_time = models.DateTimeField( blank=True, null=True)

    def transfer(self):
        dic = {}
        dic['id'] = self.id
        dic['biz_id'] = self.biz_id
        dic['biz_name'] = self.biz_name
        dic['name'] = self.name
        dic['type'] = self.type
        dic['res'] = self.res
        dic['phone'] = self.phone
        dic['test_date'] = self.test_date.strftime('%Y-%m-%d %H:%M:%S')
        dic['addr'] = self.addr
        dic['test_title'] = self.test_title
        dic['create_user'] = self.create_user
        dic['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['update_user'] = self.update_user
        dic['update_time'] = self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        return dic


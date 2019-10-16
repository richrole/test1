# -*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.

# 模板
class Template(models.Model):
    name = models.CharField(max_length = 255)
    biz_id = models.CharField(max_length = 255)
    biz_name = models.CharField(max_length = 255)
    _type = models.CharField(max_length = 255)
    create_user = models.CharField(max_length = 255)
    create_time = models.DateTimeField()
    update_user = models.CharField(max_length = 255, default = None, blank=True, null=True)
    update_time = models.DateTimeField( blank=True, null=True)

    def of(self, dict):
        self.name = dict['name']
        self.biz_id = dict['biz_id']
        self.biz_name = dict['biz_name']
        self._type = dict['_type']
        self.create_user = dict['create_user']
        self.create_time = datetime.datetime.now()
    
def temp_to_dict(temp):
    dict = {}
    dict['id'] = temp.id
    dict['name'] = temp.name
    dict['biz_id'] = temp.biz_id
    dict['biz_name'] = temp.biz_name
    dict['_type'] = temp._type
    dict['create_user'] = temp.create_user
    dict['create_time'] = temp.create_time.__str__()
    dict['update_user'] = temp.update_user
    dict['update_time'] = temp.update_time.__str__()
    return dict

# 项目
class CheckList(models.Model):
    seq = models.CharField(max_length = 10)
    item = models.CharField(max_length = 512)
    remark = models.CharField(max_length = 512)
    resp = models.CharField(max_length = 128)
    template_id = models.IntegerField(blank=True, null=True)

    def of(self, dict):
        self.seq = dict['seq']
        self.item = dict['item']
        self.remark = dict['remark']
        self.resp = dict['resp']

def check_list_to_dict(checkList):
    dict = {}
    dict['id'] = checkList.id
    dict['seq'] = checkList.seq
    dict['item'] = checkList.item
    dict['remark'] = checkList.remark
    dict['resp'] = checkList.resp
    dict['template_id'] = checkList.template_id
    return dict

# 任务
class Task(models.Model):
    biz_id = models.CharField(max_length = 255)
    biz_name = models.CharField(max_length = 255)
    temp_id = models.IntegerField()
    temp_name = models.CharField(max_length = 255)
    temp_type = models.CharField(max_length = 255)
    action_num = models.CharField(max_length = 255)
    status = models.CharField(max_length = 255)
    create_user = models.CharField(max_length = 255, default = None)
    create_time = models.DateTimeField(default = None)
    update_user = models.CharField(max_length = 255, default = None, blank=True, null=True)
    update_time = models.DateTimeField(default = None, blank=True, null=True)
    
    def of(self, dict):
        self.biz_id = dict['biz_id']
        self.biz_name = dict['biz_name']
        self.temp_id = dict['temp_id']
        self.temp_name = dict['temp_name']
        self.temp_type = dict['temp_type']
        self.action_num = dict['action_num']
        # self.status = dict['status']
        self.create_user = dict['create_user']
        self.create_time = datetime.datetime.now()

def task_to_dict(task):
    dict = {}
    dict['id'] = task.id
    dict['biz_id'] = task.biz_id
    dict['biz_name'] = task.biz_name
    dict['temp_id'] = task.temp_id
    dict['temp_name'] = task.temp_name
    dict['temp_type'] = task.temp_type
    dict['action_num'] = task.action_num
    dict['status'] = task.status
    dict['create_user'] = task.create_user
    dict['create_time'] = task.create_time.__str__()
    dict['update_time'] = task.update_time.__str__()
    dict['update_user'] = task.update_user
    return dict

# 任务项
class TaskItem(models.Model):
    task_id = models.IntegerField()
    check_list_id = models.IntegerField()
    status = models.CharField(max_length = 255, default = None)
    confirm_user = models.CharField(max_length = 255, default = None, blank=True, null=True)
    confirm_time = models.DateTimeField(default = None, blank=True, null=True)

    def of(self, dict):
        self.task_id = dict['task_id']
        self.check_list_id = dict['check_list_id']
        self.status = dict['status']
        self.confirm_user = dict['confirm_user']
        self.confirm_time = datetime.datetime.now()

def task_item_to_dict(taskItem):
    dict = {}
    dict['id'] = taskItem.id
    dict['task_id'] = taskItem.task_id
    dict['check_list_id'] = taskItem.check_list_id
    dict['status'] = taskItem.status
    dict['confirm_user'] = taskItem.confirm_user
    dict['confirm_time'] = taskItem.confirm_time.__str__()
    return dict
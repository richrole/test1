# -*- coding: utf-8 -*-
import json

import requests
from django.http import JsonResponse
from django.core import serializers
from account.decorators import login_exempt
from common.mymako import render_mako_context
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.models import Script
# Create your views here.
from host_application.models import MornitorHost
from host_application.models import MornitorResult
from host_application.esb_helper import cc_search_biz
from host_application.esb_helper import cc_search_host
from host_application.esb_helper import run_fast_execute_script
from host_application.esb_helper import get_job_instance_log
from celery.task import periodic_task
from celery.schedules import crontab
import datetime

from patrol_application.models import PatrolTemplate, PatrolTask


def template_page(request):
    """
    首页
    """
    return render_mako_context(request, '/patrol_application/template_page.html')
def task_page(request):
    """
    首页
    """
    return render_mako_context(request, '/patrol_application/task_page.html')

def delete(request):
    """
    删除
    """
    id = request.GET.get('id')
    PatrolTemplate.objects.filter(id=id).delete()
    return JsonResponse({'result': True})

def save_template(request):
    patrol_template = json.loads(request.body)
    PatrolTemplate.objects.create(name=patrol_template['name'],
                        biz_id=patrol_template['biz_id'],
                        biz_name=patrol_template['biz_name'],
                        content=patrol_template['content'],
                        domain=patrol_template['domain'],
                        mark=patrol_template['mark'],
                        create_time=datetime.datetime.now(),
                        update_time=datetime.datetime.now(),
                        create_user=request.user.username)
    return JsonResponse({"result": True})

# 工单列表
def template_list(request):
    """
        根据条件查询
        """
    # 判断是否传入查询参数
    queryDic = request.GET
    querySet = PatrolTemplate.objects
    condition = False
    for v in request.GET.values():
        if v != '':
            condition = True
            break
    if not condition:
        querySet = querySet.all()
    else:
        if (queryDic.get('name')):
            querySet = querySet.filter(name=queryDic.get('name'))
        if (queryDic.get('biz_name')):
            querySet = querySet.filter(biz_name=queryDic.get('biz_name'))

    result = []
    for item in querySet:
        result.append(item.transfer())

    return JsonResponse(result, safe=False)

# 工单列表
def task_list(request):
    """
        根据条件查询
        """
    # 判断是否传入查询参数
    queryDic = request.GET
    querySet = PatrolTask.objects
    condition = False
    for v in request.GET.values():
        if v != '':
            condition = True
            break
    if not condition:
        querySet = querySet.all()
    else:
        if (queryDic.get('task_name')):
            querySet = querySet.filter(task_name=queryDic.get('task_name'))
        if (queryDic.get('type')):
            querySet = querySet.filter(type=queryDic.get('type'))

    result = []
    for item in querySet:
        result.append(item.transfer())

    return JsonResponse(result, safe=False)

def task_save(request):
    task = json.loads(request.body)
    PatrolTask.objects.create(task_name=task['task_name'],
                        biz_id=task['biz_id'],
                        biz_name=task['biz_name'],
                        template_name=task['template_name'],
                        template_id=task['template_id'],
                        type=task['type'],
                        ip=task['ip'],
                        create_time=datetime.datetime.now(),
                        update_time=datetime.datetime.now(),
                        create_user=request.user.username)
    return JsonResponse({"result": True})

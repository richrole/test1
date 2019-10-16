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

def host(request):
    """
    首页
    """
    id = request.GET.get('id')
    return render_mako_context(request, '/host_application/host.html',{ "id":id})

def getBiz(request):
    data = cc_search_biz()
    data = data['data']
    result = []
    for obj in data['info']:
        result.append({'label': obj['bk_biz_name'], 'value': obj['bk_biz_id']})
    return JsonResponse({"data": result})

def searchHost(request):
    result = []
    biz_id = request.GET.get('type')
    if biz_id is None or biz_id == "":
        return JsonResponse({"data": result})
    data = cc_search_host(biz_id, None)
    data = data['data']
    data = data['info']
    for obj in data:
        result.append(obj['host'])
    return JsonResponse({"data": result})

def executeScript(request):
    acceptData = json.loads(request.body)
    biz_id = acceptData['bizId']
    script_content = acceptData['scriptContent']
    ip_list = acceptData['ipList']
    ipList =[]
    for ip in ip_list:
        ipData ={
            'ip': ip['ip'],
            'bk_cloud_id':ip['bk_cloud_id']
        }
        ipList.append(ipData)
    result = run_fast_execute_script(biz_id, script_content, ipList)
    return JsonResponse({"data": result})

def searchScriptResult(request):
    biz_id = request.GET.get('bizId')
    job_instance_id = request.GET.get('jobInstanceId')
    result = get_job_instance_log(biz_id, job_instance_id)
    return JsonResponse({"data": result})

def saveHost(request):
    hostForm = json.loads(request.body)
    querySet = MornitorHost.objects
    querySet = querySet.filter(ip=hostForm['ip'])
    if len(querySet):
        return JsonResponse({"result": True})
    content = "MEMORY=$(free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }');DISK=$(df -h | awk '$NF==\"/\"{printf \"%s\", $5}');CPU=$(top -bn1 | grep load | awk '{printf \"%.2f%%\", $(NF-2)}');DATE=$(date '+%Y-%m-%d %H:%M:%S');echo -e \"$DATE|$MEMORY|$DISK|$CPU\""
    MornitorHost.objects.create(biz_id=hostForm['bizId'],ip=hostForm['ip'],content = content,cloud_id = hostForm['cloudId'])
    return JsonResponse({"result": True})

def monitorDetail(request):
    """
        根据条件查询
        """
    # 判断是否传入查询参数
    condition = False
    for v in request.GET.values():
        if v != '':
            condition = True
            break

    querySet = MornitorResult.objects
    if not condition:
        querySet = querySet.all()
    else:
        end_time = datetime.datetime.now()
        start_time = datetime.datetime.now() + datetime.timedelta(hours=-0.5)
        queryDic = request.GET
        if (queryDic.get('ip')):
            querySet = querySet.filter(ip=queryDic.get('ip'))
        querySet = querySet.filter(created_time__gte=start_time)
        querySet = querySet.filter(created_time__lte=end_time)
    result = []
    for item in querySet:
        result.append(item.transfer())
    return JsonResponse(result, safe=False)

@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def executeMonitor():
    querySet = MornitorHost.objects
    querySet = querySet.all()
    for item in querySet:
        ipList = []
        ipData = {
            'ip': item.ip,
            'bk_cloud_id': item.cloud_id
        }
        ipList.append(ipData)
        # 执行脚本
        result = run_fast_execute_script(item.biz_id, item.content, ipList)
        job_instance_id = result['data']
        # 获得执行结果
        log_result = get_job_instance_log(item.biz_id, job_instance_id)
        for log in log_result:
            if (log['is_success']):
                messageList = log['log_content'].split("|")
                # 把“”去掉
                mapResult = [x.strip() for x in messageList if x.strip() != '']
                # 执行结果分割
                memory = mapResult[1].strip('%')
                disk = mapResult[2].strip('%')
                cpu = mapResult[3].strip('%')
                # 将执行结果保存到表中
                MornitorResult.objects.create(ip=item.ip, memory=memory, disk=disk, cpu=cpu)
    return JsonResponse({"result": True})

# 测试接口是否能成功
def testMonitor(request):
    print "test"
    querySet = MornitorHost.objects
    querySet = querySet.all()
    for item in querySet:
        ipList = []
        ipData = {
            'ip': item.ip,
            'bk_cloud_id': item.cloud_id
        }
        ipList.append(ipData)
        # 执行脚本
        result = run_fast_execute_script(item.biz_id, item.content, ipList)
        job_instance_id = result['data']
        # 获得执行结果
        log_result = get_job_instance_log(item.biz_id, job_instance_id)
        for log in log_result:
            if (log['is_success']):
                messageList = log['log_content'].split("|")
                mapResult = [x.strip() for x in messageList if x.strip() != '']
                # 执行结果分割
                memory = mapResult[1].strip('%')
                disk = mapResult[2].strip('%')
                cpu = mapResult[3].strip('%')
                # 将执行结果保存到表中
                MornitorResult.objects.create(ip=item.ip, memory=memory, disk=disk, cpu=cpu)
    return JsonResponse({"result": True})

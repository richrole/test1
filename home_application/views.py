# -*- coding: utf-8 -*-
import datetime
import json

import requests
from django.http import JsonResponse
from django.core import serializers
from account.decorators import login_exempt
from common.mymako import render_mako_context
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.models import Script
from home_application.esb_helper import get_app_info
# Create your views here.



def home(request):
    """
    首页
    """
    id = request.GET.get('id')
    #考试放开即可 return render_mako_context(request, '/home_application/home.html',{ "id":id})
    return render_mako_context(request, '/bk_application/test.html', {"id": id})

def test(request):
    """
    测试

    obj = request.GET
    if len(obj) > 2:
        return JsonResponse({'result': False, "message": "ok"})
    else:
        return JsonResponse({'result': True, "message": "ok"})
    """
    data = request.GET.values
    # data = {
    #     'username': request.user.username,
    #     'time': datetime.datetime.now()
    # }
    return JsonResponse({'result': True, 'data':data})

def get_app_info(request):
    ##data = get_app_info()
    data = {
        "result": True,
        "code": 0,
        "message": "",
        "request_id": '0abee074-29dc-4723-8fd7-f387b9f54e67',
        "data": [
            {
                "bk_app_code": "bk_test",
                "bk_app_name": "BKTest"
            },
            {
                "bk_app_code": "esb_test",
                "bk_app_name": "ESBTest"
            }
        ]
    }
    return JsonResponse({'result': True, 'data':data})

def rest(request):
    method = request.method
    if method == 'GET':
        return search(request)
    elif method == "POST":
        return create(request)
    elif method == "PUT":
        return update(request)

def find_all(request):
    """
    根据条件查询所有脚本
    """

def create(request):
    """
    创建脚本
    """
    a = 1
    script = json.loads(request.body)
    Script.objects.create(name=script['name'], desc=script['desc'], type = script['type'], source = script['source'], content = script['content'], version = a)
    return JsonResponse({"result": True})

def update(request):
    """
    更新脚本
    """
    params = json.loads(request.body)
    print type(params)
    script = Script.objects.get(id=params['id'])
    script.name = params['name']
    script.desc=params['desc']
    script.type=params['type']
    script.source=params['source']
    script.content=params['content']
    script.version=params['version']
    script.save()
    return JsonResponse({'result': True})

def search(request):
    """
    根据条件查询
    """
    # 判断是否传入查询参数
    condition = False
    for v in request.GET.values():
        if v != '' :
            condition = True
            break

    querySet = Script.objects
    if not condition:
        querySet = querySet.all()
    else:
        queryDic = request.GET
        if (queryDic.get('name')):
            querySet = querySet.filter(name=queryDic.get('name'))
        if (queryDic.get('creator')):
            querySet = querySet.filter(creator=queryDic.get('creator'))
        if (queryDic.get('time')):
            querySet = querySet.filter(time=queryDic.get('time'))
        if (queryDic.get('type')):
            querySet = querySet.filter(type=queryDic.get('type'))
        if (queryDic.get('source')):
            querySet = querySet.filter(source=queryDic.get('source'))
        if (queryDic.get('start_time')):
            querySet = querySet.filter(created_time__gte=queryDic.get('start_time').replace('&nbsp;', ' '))
        if (queryDic.get('end_time')):
            querySet = querySet.filter(created_time__lte=queryDic.get('end_time').replace('&nbsp;', ' '))

    result = []
    for item in querySet:
        result.append(item.transfer())

    return JsonResponse(result, safe=False)

def rest_with_args(request, id):
    method = request.method
    if method == 'GET':
        return find_one(request, id)
    elif method == "DELETE":
        return delete(request, id)

def find_one(request, id):
    """
    根据ID查询脚本
    """
    script = Script.objects.get(id=id)
    
    return JsonResponse(script.transfer(), safe=False)

def delete(request, id):
    """
    删除脚本
    """
    Script.objects.filter(id=id).delete()
    return JsonResponse({'result': True})
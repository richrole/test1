# -*- coding: utf-8 -*-
import datetime
import json
import requests
from django.http import JsonResponse
from common.mymako import render_mako_context
from host_application.esb_helper import cc_search_user

# Create your views here.
from work_application.models import Work


def work(request):
    return render_mako_context(request, "/work_application/work_manage.html")

def approval(request):
    return render_mako_context(request, '/work_application/approval_list.html')

def save(request):
    work = json.loads(request.body)
    Work.objects.create(title=work['title'],
                        approver=work['approver'],
                        biz_id=work['biz_id'],
                        biz_name=work['biz_name'],
                        ip=work['ip'],
                        content=work['content'],
                        status=work['status'],
                        create_time=datetime.datetime.now(),
                        update_time=datetime.datetime.now(),
                        create_user=request.user.username)
    return JsonResponse({"result": True})

def update(request):
    """
        更新
        """
    params = json.loads(request.body)
    print type(params)
    work = Work.objects.get(id=params['id'])
    work.title = params['title']
    work.approver = params['approver']
    work.biz_id = params['biz_id']
    work.biz_name = params['biz_name']
    work.ip = params['ip']
    work.content = params['content']
    work.status = params['status']
    work.update_user = request.user.username
    work.update_time = datetime.datetime.now()
    work.save()
    return JsonResponse({'result': True})

# 工单列表
def list(request):
    """
        根据条件查询
        """
    # 判断是否传入查询参数
    queryDic = request.GET
    querySet = Work.objects
    condition = False
    for v in request.GET.values():
        if v != '':
            condition = True
            break
    if not condition:
        querySet = querySet.all()
    else:
        if (queryDic.get('title')):
            querySet = querySet.filter(title=queryDic.get('title'))
        if (queryDic.get('status')):
            querySet = querySet.filter(status=queryDic.get('status'))

    result = []
    for item in querySet:
        result.append(item.transfer())

    return JsonResponse(result, safe=False)

def detail(request):
    id = request.GET.get('id')
    work = Work.objects.get(id=id)
    return JsonResponse(work.transfer(), safe=False)

# 审批列表
def approvals(request):
    """
        根据条件查询
        """
    # 判断是否传入查询参数
    queryDic = request.GET
    querySet = Work.objects
    condition = False
    for v in request.GET.values():
        if v != '':
            condition = True
            break
    if not condition:
        querySet = querySet.filter(status='审核中')
    else:
        if (queryDic.get('title')):
            querySet = querySet.filter(title=queryDic.get('title'))
        if (queryDic.get('status')):
            querySet = querySet.filter(status=queryDic.get('status'))

    result = []
    for item in querySet:
        result.append(item.transfer())

    return JsonResponse(result, safe=False)

def approve(request):
    """
        审批
        """
    params = json.loads(request.body)
    print type(params)
    work = Work.objects.get(id=params['id'])
    work.status = params['status']
    if params['refuse'] == 'refuse':
        work.rejection = params['rejection']
    work.update_user = request.user.username
    work.update_time = datetime.datetime.now()
    work.save()
    return JsonResponse({'result': True})

def delete(request):
    """
    删除
    """
    id = request.GET.get('id')
    Work.objects.filter(id=id).delete()
    return JsonResponse({'result': True})

def users(request):
    data = cc_search_user()
    data = data['data']
    print data
    return JsonResponse(data, safe=False)
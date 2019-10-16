# -*- coding: utf-8 -*-
from django.shortcuts import render
import json
import time
import os
import StringIO
import xlrd
import uuid
import datetime
import xlsxwriter

import requests
from django.http import JsonResponse, HttpResponse

from account.decorators import login_exempt
from common.mymako import render_mako_context
from  common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from .models import Template,CheckList,Task,TaskItem,temp_to_dict,check_list_to_dict,task_to_dict,task_item_to_dict

# Create your views here.


def test_api(request):
    data = request.GET
    result = {}
    result['result'] = True
    result['success'] = 'success'
    result['data'] = data
    return JsonResponse(result)

def template(request):
    return render_mako_context(request, "/task_application/task_template.html")

def center(request):
    return render_mako_context(request, '/task_application/task_center.html')

def temp_list(request):
    body = request.GET
    condition = False
    for val in body.values():
        if (val != ''):
            condition = True
            break
    
    if(not condition):
        dict_arr = []
        objs = Template.objects.all()
        for o in objs:
            dict_arr.append(temp_to_dict(o))
        return JsonResponse({'result': True, 'success': 'success', 'data': dict_arr})
    else:
        query = Template.objects
        if(body['biz_id'] != ''):
            query = query.filter(biz_id = body['biz_id'])
        if(body['name'] != ''):
            query = query.filter(name__contains = body['name'])
        if(body['_type'] != ''):
            query = query.filter(_type = body['_type'])
        
        data_list = []
        for o in query:
            data_list.append(temp_to_dict(o))
        return JsonResponse({'result': True, 'data': data_list})


def file_upload(request):
    data = xlrd.open_workbook(filename = None, file_contents = request.FILES['file'].read())
    table = data.sheets()[0]
    nrows = table.nrows
    index_list = ['seq', 'item', 'remark', 'resp']
    id_list = []
    for i in range(1, nrows):
        data_dict = {}
        table_row_values = table.row_values(i)
        for j in range(table_row_values.__len__()):
            data_dict[index_list[j]] = table_row_values[j]
        ck = CheckList(seq = '', item = '', remark = '', resp = '', template_id = None)
        ck.of(data_dict)
        ck.save()
        id_list.append(ck.id)   
    return JsonResponse({'result': True, 'data': id_list})

def save_temp(request):
    body = json.loads(request.body)
    body['create_user'] = request.user.username
    temp = Template(name = '', biz_id = '', biz_name = '', _type = '', create_user = '', create_time = None, update_user = '', update_time = None)
    temp.of(body)
    temp.save()
    temp_id = temp.id

    for ck_id in body['ck_list']:
        ck = CheckList.objects.get(id = ck_id)
        ck.template_id = temp_id
        ck.save()
    
    return JsonResponse({'result': True, 'data': temp_id})

def save_task(request):
    body = json.loads(request.body)
    body['create_user'] = request.user.username
    task = Task(biz_id = '', biz_name = '', temp_id = None, temp_name = '', temp_type = '', action_num = '', status = '待操作', create_user = '', create_time = None, update_user = '', update_time = None)
    task.of(body)
    task.save()
    lists = CheckList.objects.filter(template_id = body['temp_id'])
    for o in lists:
        TaskItem(task_id = task.id, check_list_id = o.id, status = u'待操作', confirm_user = '', confirm_time = None).save()

    return JsonResponse({'result': True, 'data': task.id})

def check_list(request):
    temp_id = request.GET.get('temp_id')
    obj_list = CheckList.objects.filter(template_id = temp_id)
    data_list = []
    for o in obj_list:
        dict = check_list_to_dict(o)
        data_list.append(dict)
    
    return JsonResponse({'result': True, 'data': data_list})

# 任务列表查看任务详情
def check_list_more(request):
    temp_id = request.GET.get('temp_id')
    task_id = request.GET.get('task_id')
    obj_list = CheckList.objects.filter(template_id = temp_id)
    data_list = []
    for o in obj_list:
        taskItem = TaskItem.objects.filter(check_list_id = o.id).filter(task_id = task_id)[0]
        dict = check_list_to_dict(o)
        dict['status'] = taskItem.status
        dict['confirm_user'] = taskItem.confirm_user
        dict['confirm_time'] = taskItem.confirm_time.__str__()
        # print dict['status']
        dict['disabled'] = (dict['status'] == u'已完成')
        dict['taskItemId'] = taskItem.id
        data_list.append(dict)
    
    return JsonResponse({'result': True, 'data': data_list})

def task_list(request):
    body = request.GET
    condition = False
    for val in body.values():
        if (val != ''):
            condition = True
            break
    
    print body['action_num']
    user = request.user.username
    if(not condition):
        obj_list = Task.objects.filter(create_user = user)
        data_list = []
        for o in obj_list:
            dict = task_to_dict(o)
            data_list.append(dict)
        return JsonResponse({'result': True, 'data': data_list})
    else:
        query = Task.objects
        if(body['biz_id'] != ''):
            query = query.filter(biz_id = body['biz_id'])
        if(body['temp_type'] != ''):
            query = query.filter(temp_type = body['temp_type'])
        if(body['status'] != ''):
            query = query.filter(status = body['status'])
        if(body['create_user'] != ''):
            query = query.filter(create_user__contains = body['create_user'])
        if(body['temp_name'] != ''):
            query = query.filter(temp_name__contains = body['temp_name'])
        if(body['action_num'] != ''):
            query = query.filter(action_num__contains = body['action_num'])
        data_list = []
        for o in query:
            dict = task_to_dict(o)
            data_list.append(dict)
        return JsonResponse({'result': True, 'data': data_list})

def delete(request):
    params = request.GET
    id = params['id']
    Template.objects.get(id = id).delete()
    CheckList.objects.filter(template_id = id).delete()
    Task.objects.filter(temp_id = id).delete()
    return JsonResponse({'result': True})

def confirm_task(request):
    taskItemId = request.GET.get('taskItemId')
    taskItem = TaskItem.objects.get(id = taskItemId)
    taskItem.confirm_user = request.user.username
    taskItem.confirm_time = datetime.datetime.now()
    taskItem.status = u'已完成'
    taskItem.save()

    # 计算task的状态
    task = Task.objects.get(id = taskItem.task_id)
    underAction = 0
    complete = 0
    items = TaskItem.objects.filter(task_id = taskItem.task_id)
    for item in items:
        if(item.status == u'待操作'):
            underAction = underAction + 1
        if(item.status == u'已完成'):
            complete = complete + 1
    
    if(underAction > 0 and complete > 0):
        task.status = u'操作中'
    if(underAction > 0 and complete == 0):
        task.status = u'待操作'
    if(underAction == 0 and complete > 0):
        task.status = u'已完成'
    task.save()
    return JsonResponse({'result': True})

def download(request):
    id = request.GET.get('temp_id')
    obj_arr = CheckList.objects.filter(template_id = id)
    data_list = []
    for o in obj_arr:
        dict = check_list_to_dict(o)
        dict.pop('id')
        dict.pop('template_id')
        data_list.append(dict)
    data_key = ['seq', 'item', 'remark', 'resp']
    return make_excel(data_list, data_key, 'template')

# 生成Excel文件
def make_excel(get_data, data_key,get_file_name):
    sio = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(sio)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format({
        'num_format': '@',
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })
    dict = {}
    dict['seq'] = u'序号'
    dict['item'] = u'操作项目'
    dict['remark'] = u'备注'
    dict['resp'] = u'责任人'
    for index in range(data_key.__len__()):
        key = data_key[index]
        worksheet.write(0, index, dict[key], header_format)
    cols_num = get_data.__len__()
    rows_num = get_data[0].keys().__len__()
    itemlist = data_key
    for col in range(cols_num):
        for row in range(rows_num):
            data = get_data[col][itemlist[row]]
            if row == 0:
                with_op = 10
            else:
                with_op = 20
            worksheet.set_column(col + 1, row, with_op)
            if type(data) == dict:
                worksheet.write(col + 1, row, data['name'], header_format)
                worksheet.data_validation(col, row, col, row, {'validate': 'list', 'source': data['list']})
            else:
                if itemlist[row] == 'vm_expired_time':
                    if data == '0':
                        worksheet.write(col + 1, row, '', header_format)
                    else:
                        worksheet.write(col + 1, row, data, header_format)
                else:
                    worksheet.write(col + 1, row, data, header_format)
    workbook.close()
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='APPLICATION/OCTET-STREAM')
    file_name = 'attachment; filename=%s.xlsx'%(get_file_name)
    response['Content-Disposition'] = file_name
    return response

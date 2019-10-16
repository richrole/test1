# -*- coding: utf-8 -*-
import json
from StringIO import StringIO

import requests
import xlsxwriter
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from account.decorators import login_exempt
from common.mymako import render_mako_context
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.models import Script
# Create your views here.
from bk_application.models import Test
from bk_application.esb_helper import cc_search_biz
from bk_application.esb_helper import cc_search_host
from bk_application.esb_helper import run_fast_execute_script
from bk_application.esb_helper import get_job_instance_log
from celery.task import periodic_task
from celery.schedules import crontab
import datetime

# 考试页面
def test(request):
    """
    首页
    """
    return render_mako_context(request, '/bk_application/test.html')

# 蓝鲸业务
def get_biz(request):
    data = cc_search_biz()
    data = data['data']
    result = []
    for obj in data['info']:
        result.append({'label': obj['bk_biz_name'], 'value': obj['bk_biz_id']})
    return JsonResponse({"data": result})

# 列表
def list(request):
    """
        根据条件查询
        """
    # 判断是否传入查询参数
    condition = False
    for v in request.GET.values():
        if v != '':
            condition = True
            break

    querySet = Script.objects
    if not condition:
        querySet = querySet.all()
    else:
        queryDic = request.GET
        if (queryDic.get('name')):
            querySet = querySet.filter(name=queryDic.get('name'))
        if (queryDic.get('start_time')):
            querySet = querySet.filter(created_time__gte=queryDic.get('start_time').replace('&nbsp;', ' '))
        if (queryDic.get('end_time')):
            querySet = querySet.filter(created_time__lte=queryDic.get('end_time').replace('&nbsp;', ' '))

    result = []
    for item in querySet:
        result.append(item.transfer())

    return JsonResponse(result, safe=False)

# 保存
def save(request):
    """
    创建脚本
    """
    test_obj = json.loads(request.body)
    Test.objects.create(title=test_obj['title'],
                        approver=test_obj['approver'],
                        biz_id=test_obj['biz_id'],
                        create_time=datetime.datetime.now(),
                        update_time=datetime.datetime.now(),
                        create_user=request.user.username)
    return JsonResponse({"result": True})

# 修改
def update(request):
    """
    更新
    """
    params = json.loads(request.body)
    print type(params)
    test_obj = Test.objects.get(id=params['id'])
    test_obj.title = params['title']
    test_obj.update_user = request.user.username
    test_obj.update_time = datetime.datetime.now()
    test_obj.save()
    return JsonResponse({'result': True})

# 删除
def delete(request):
    test_id = request.GET.get('id')
    Test.objects.filter(id=test_id).delete()

# 上传
def upload(request):
    result = []

    return JsonResponse({"data": result})

# 下载
def download(request):
    id = request.GET.get('temp_id')
    obj_arr = Test.objects.filter(template_id=id)
    data_list = []
    for o in obj_arr:
        # dict = check_list_to_dict(o)
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
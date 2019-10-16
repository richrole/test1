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



#上传文件
def upload(request):
    """
    创建
    :param request:
    :return:
    """
    name = request.FILES['file'].name
    file = open(name, 'wb')
    file.write(request.FILES['file'].read())
    return JsonResponse({'result': True})
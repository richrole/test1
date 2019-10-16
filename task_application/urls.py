# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'task_application.views',
    (r'^tonychen/api/test/$', 'test_api'),
    (r'^template/$', 'template'),
    (r'^temp_list/$', 'temp_list'),
    (r'^file_upload/$', 'file_upload'),
    (r'^save_temp/$', 'save_temp'),
    (r'^delete/$', 'delete'),
    (r'^save_task/$', 'save_task'),
    (r'^check_list/$', 'check_list'),
    (r'^center/$', 'center'),
    (r'^task_list/$', 'task_list'),
    (r'^check_list_more/$', 'check_list_more'),
    (r'^confirm_task/$', 'confirm_task'),
    (r'^download/$', 'download')
)

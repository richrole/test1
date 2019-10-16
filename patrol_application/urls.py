# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'patrol_application.views',
    (r'^template/$', 'template_page'),
    (r'^task/$', 'task_page'),
    (r'^delete/$', 'delete'),
    (r'^template_list/$', 'template_list'),
    (r'^save_template/$', 'save_template'),
    (r'^task_list/$', 'task_list'),
    (r'^task_save/$', 'task_save'),

)

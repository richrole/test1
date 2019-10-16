# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'work_application.views',
    (r'^work/$', 'work'),
    (r'^approval/$', 'approval'),
    (r'^save/$', 'save'),
    (r'^update/$', 'update'),
    (r'^list/$', 'list'),
    (r'^detail/$', 'detail'),
    (r'^approvals/$', 'approvals'),
    (r'^approve/$', 'approve'),
    (r'^users/$', 'users'),
    (r'^delete/$', 'delete'),

)

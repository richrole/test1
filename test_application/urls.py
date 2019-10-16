# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'test_application.views',
    (r'^test_page/$', 'test_page'),
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

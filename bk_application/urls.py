# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'bk_application.views',
    (r'^test/$', 'test'),
    (r'^biz/$', 'get_biz'),
    (r'^list/$', 'list'),
    (r'^execute/$', 'executeScript'),
    (r'^result/$', 'searchScriptResult'),
    (r'^summit/$', 'saveHost'),
    (r'^monitor/$', 'monitorDetail'),
    (r'^$', 'host')
)

# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'host_application.views',
    (r'^biz/$', 'getBiz'),
    (r'^list/$', 'searchHost'),
    (r'^execute/$', 'executeScript'),
    (r'^result/$', 'searchScriptResult'),
    (r'^summit/$', 'saveHost'),
    (r'^monitor/$', 'monitorDetail'),
    (r'^test/$', 'testMonitor'),
    (r'^$', 'host')
)

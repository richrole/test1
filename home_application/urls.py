# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^get_app_info/$', 'get_app_info'),
    (r'^api/test/$', 'test'),
    (r'^script/$', 'rest'),
    (r'^script/(\d+)$', 'rest_with_args')
)

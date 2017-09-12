# -*- coding:utf8 -*-

from django.conf.urls import url
from . import views

urlpatterns= [
    url(
        r'^terminals/$', views.get_post_terminal, name='get_post_terminal'
    ),
    url(
        r'^terminals/(?P<pk>\w+)/$', views.get_patch_single_terminal, name='get_patch_single_terminal'
    ),
    url(
        r'^terminals/(?P<pk>\w+)/climate/$', views.get_post_climate, name='get_post_climate'
    ),
    url(
        r'^terminals/(?P<pk1>\w+)/climate/(?P<pk2>(0|0?[1-9]|1[0-9]|2[0-3]))/$', views.get_hours_climate, name='get_hours_climate'
    ),
    url(
        r'^terminals/(?P<pk1>\w+)/climate/day/(?P<pk2>\d{4}-\d{1,2}-\d{1,2})/$', views.get_day_climate, name='get_day_climate'
    ),

     url(
        r'^terminals/(?P<pk>\w+)/climate/days/(?P<begin>\d{4}-\d{1,2}-\d{1,2})/(?P<end>\d{4}-\d{1,2}-\d{1,2})/$', views.get_week_climate, name='get_week_climate'
    ),

    url(
        r'^users/$', views.get_post_user, name='get_post_user'
    ),
    url(
        r'^users/(?P<pk>\w+)/$', views.get_patch_single_user, name='get_patch_single_user'
    ),
    url(
        r'^city/$', views.post_city, name='post_city'
    ),
    url(
        r'^post/$', views.save_climate, name='save_climate'
    ),


]

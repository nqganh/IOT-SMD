from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from tastypie.api import Api
from device.resources import UserResource, DeviceResource, RingGroupResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(DeviceResource())
v1_api.register(RingGroupResource())

from user.views import (
    HomePageView,
    LoginView,
    ProfileUpdate,
    AccountList,
    AccountAdd,
    AccountUpdate,
    AccountDelete,
)
from device import views
from device.views import(
    DeviceList,
    DeviceAdd,
    DeviceUpdate,
    DeviceDelete,
    RGList, 
    RGAdd,
    RGUpdate,
    RGDelete,
    RGDList,
    RGDAdd,
    RGDDelete,
    RGDUpdate,
    RGDCreate,
    load_rguuid,
    load_destinationnumber,
)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'expex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', TemplateView.as_view(template_name="homepage.html")),
    url(r'^$', HomePageView.as_view(), name='home'),
    (r'^api/', include(v1_api.urls)),

    url(r'^accounts/logout/$', logout, {'next_page': '/accounts/login' }, name='acct_logout'),
    url(r'^accounts/login/$', LoginView.as_view(), name='acct_login'),

    url(r'^user/accounts/$', AccountList.as_view(), name='account_list'),
    url(r'^user/accounts/add/$', AccountAdd.as_view(), name='account_add'),
    url(r'^user/accounts/(?P<pk>\d+)/edit$', AccountUpdate.as_view(), name='account_edit'),
    url(r'^user/accounts/(?P<pk>\d+)/delete$', AccountDelete.as_view(), name='account_delete'),

    url(r'^user/devices/$', DeviceList.as_view(), name='device_list'),
    url(r'^user/devices/add/$', DeviceAdd.as_view(), name='device_add'),
    url(r'^user/devices/(?P<uuid>[0-9a-f-]+)/edit$', DeviceUpdate.as_view(), name='device_edit'),
    url(r'^user/devices/(?P<uuid>[0-9a-f-]+)/delete$', DeviceDelete.as_view(), name='device_delete'),
    
    url(r'^user/rgroupl/$', RGList.as_view(), name='department_list'),    
    url(r'^user/rgroupl/add/$', RGAdd.as_view(), name='department_add'),
    url(r'^user/rgroupl/(?P<uuid>[0-9a-f-]+)/delete$', RGDelete.as_view(), name='department_delete'),
    url(r'^user/rgroupl/(?P<uuid>[0-9a-f-]+)/edit$', RGUpdate.as_view(), name='department_edit'),
    url(r'^user/rgroupdes/$', RGDList.as_view(), name='rgd_list'),
    url(r'^user/rgroupdes/add/$', RGDAdd.as_view(), name='rgd_add'),
    url(r'^user/rgroupdes/(?P<uuid>[0-9a-f-]+)/delete$', RGDDelete.as_view(), name='rgd_delete'),
    url(r'^user/rgroupdes/(?P<uuid>[0-9a-f-]+)/edit$', RGDUpdate.as_view(), name='rgd_edit'),
    url(r'^user/rgroupdes/create/$', RGDCreate.as_view(), name='rgd_create'),
    url(r'^ajax/load-desnum/$', views.load_destinationnumber, name='ajax_load_destinationnumber'),
    url(r'^ajax/load-rguuid/$', views.load_rguuid, name='ajax_load_rguuid'),

    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    url(r'^profile/$', ProfileUpdate.as_view(), name='profile'),
)

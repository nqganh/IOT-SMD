from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from user.views import (
    HomePageView,
    LoginView,
    ProfileUpdate,
    AccountList,
    AccountAdd,
    AccountUpdate,
    AccountDelete,
)

from device.views import(
    DeviceList,
    DeviceAdd,
    DeviceUpdate,
    DeviceDelete,
)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'expex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', TemplateView.as_view(template_name="homepage.html")),
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^accounts/logout/$', logout, {'next_page': '/accounts/login' }, name='acct_logout'),
    url(r'^accounts/login/$', LoginView.as_view(), name='acct_login'),

    url(r'^user/accounts/$', AccountList.as_view(), name='account_list'),
    url(r'^user/accounts/add/$', AccountAdd.as_view(), name='account_add'),
    url(r'^user/accounts/(?P<pk>\d+)/edit$', AccountUpdate.as_view(), name='account_edit'),
    url(r'^user/accounts/(?P<pk>\d+)/delete$', AccountDelete.as_view(), name='account_delete'),

    url(r'^user/devices/$', DeviceList.as_view(), name='device_list'),
    url(r'^user/devices/add/$', DeviceAdd.as_view(), name='device_add'),
    url(r'^user/devices/(?P<pk>\d+)/edit$', DeviceUpdate.as_view(), name='device_edit'),
    url(r'^user/devices/(?P<pk>\d+)/delete$', DeviceDelete.as_view(), name='device_delete'),
    
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    url(r'^profile/$', ProfileUpdate.as_view(), name='profile'),
)

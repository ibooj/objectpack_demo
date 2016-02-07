from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from m3 import get_app_urlpatterns
from m3_ext.views import workspace


import wsfactory.urls

admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^$', login_required(
                           workspace(template='workspace.html'))),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
                           name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {
                               # 'next_page': '/login/',
                               'template_name': 'logout.html'
                           },
                           name='logout'),
                       # url(r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += get_app_urlpatterns()
urlpatterns += wsfactory.urls.urlpatterns

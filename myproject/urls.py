"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from travel.views import login, newaccount, mainpage, recommend, foot, fillinformation, security, commentview, information, willgo, myteam, travel_details, travel_leave, travel_delete, photos, allcomments
urlpatterns = [
	url(r'^site_media/(?P<path>.*)','django.views.static.serve',{'document_root':'../static/css'}),
	url(r'^([^/]+)/([^/]+)/photos/$', photos),
	url(r'^([^/]+)/([^/]+)/([^/]+)/details/$', travel_details),
	url(r'^([^/]+)/([^/]+)/([^/]+)/delete/$', travel_delete),
	url(r'^([^/]+)/([^/]+)/([^/]+)/leave/$', travel_leave),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', login),
	url(r'^newaccount/$', newaccount),
	url(r'^([^/]+)/main/$', mainpage),
	url(r'^([^/]+)/recommend/$', recommend),
	url(r'^([^/]+)/foot/$', foot),
	url(r'^([^/]+)/fillinformation/$', fillinformation),
	url(r'^([^/]+)/security/$', security),
	url(r'^([^/]+)/willgo/$', willgo),
	url(r'^([^/]+)/([^/]+)/commentview/$', commentview),
	url(r'^([^/]+)/information/$', information),
	url(r'^([^/]+)/myteam/$', myteam),
	url(r'^([^/]+)/newcomment/$', allcomments),
	url(r'^static/css/(?P<path>.*)', 'django.views.static.serve',{'document_root':settings.CSS_DIR}),
]
from django.conf.urls import patterns, url

from items import views

urlpatterns = patterns('',
    url(r'^$', views.itemlist),
    url(r'^getItems$', views.getItems),
    url(r'^computeSummary$', views.computeSummary),
)

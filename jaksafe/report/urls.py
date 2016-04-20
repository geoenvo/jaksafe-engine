from django.conf.urls import patterns, url
from report import views

urlpatterns = patterns('',
    url(r'^home/$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^auto/$', views.report_auto, name='report_auto'),
    url(r'^adhoc/$', views.report_adhoc, name='report_adhoc'),
    url(r'^flood/$', views.report_flood, name='report_flood'),
    url(r'^impact_config/$', views.report_impact_config, name='report_impact_config'),
    url(r'^assumptions_config/$', views.report_assumptions_config, name='report_assumptions_config'),
    url(r'^aggregate_config/$', views.report_aggregate_config, name='report_aggregate_config'),
    url(r'^boundary_config/$', views.report_boundary_config, name='report_boundary_config'),
    url(r'^exposure_config/$', views.report_exposure_config, name='report_exposure_config'),
    url(r'^global_config/$', views.report_global_config, name='report_global_config'),
    url(r'^login/$', views.report_login, name='report_login'),
    url(r'^logout/$', views.report_logout, name='report_logout'),
#url for interacitive repor per event	
    url(r'^adhoc_report/(?P<id_event>[0-9]+)/$', views.report_adhoc_web, name='report_adhoc_web'),
    url(r'^auto_report/(?P<id_event>[0-9]+)/$', views.report_auto_web, name='report_auto_web'),
    url(r'^adhoc_report_xml/(?P<id_event>[0-9]+)/$', views.report_adhoc_xml, name='report_adhoc_xml'),
    url(r'^auto_report_xml/(?P<id_event>[0-9]+)/$', views.report_auto_xml, name='report_auto_xml'),
    url(r'^auto_report_json/(?P<event_date>[0-9]+)/all$', views.auto_report_json, name='auto_report_json')
)

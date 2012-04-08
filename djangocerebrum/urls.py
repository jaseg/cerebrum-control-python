from django.conf.urls import patterns, include, url
from djangocerebrum.cerebrum import views, panel_driver

log = logging.getLogger()
log.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log.debug("Loading url patterns")
log.debug("Le interface: ", views.PanelDriverRpcWrapper.getInterface(panel_driver.PanelDriver.driver))

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'djangocerebrum.cerebrum.views.home'),
    # url(r'^djangocerebrum/', include('djangocerebrum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^direct/rest/$', views.PanelDriverRestView.as_view(), name='panel-driver'),
    url(r'^direct/rest/lamp/(?P<num>[0-9]+)/$', views.PanelLampRestView.as_view(), name='panel-lamp'),
    url(r'^direct/rest/meter/(?P<num>[0-9]+)/$', views.PanelMeterRestView.as_view(), name='panel-meter'),
    url(r'^direct/rpc/$', views.PanelDriverRpcWrapper.getInterface(panel_driver.PanelDriver.driver), name='panel-rpc'),
)

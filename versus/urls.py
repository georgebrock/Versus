from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from core.views import HomepageView
from foursquare.views import StartAuthView, CompleteAuthView

urlpatterns = patterns('',
    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^login/', StartAuthView.as_view(), name='login'),
    url(r'^authenticated/', CompleteAuthView.as_view(), name='login-complete'),

    # Examples:
    # url(r'^$', 'versus.views.home', name='home'),
    # url(r'^versus/', include('versus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

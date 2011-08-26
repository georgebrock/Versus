from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from core.views import HomepageView, CompareView
from foursquare.views import StartAuthView, CompleteAuthView, LogoutView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomepageView.as_view(), name='home'),

    url(r'^login/', StartAuthView.as_view(), name='login'),
    url(r'^authenticated/', CompleteAuthView.as_view(), name='login-complete'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),

    url(r'^compare/', login_required(CompareView.as_view(), login_url='/login/'), name='compare'),

    # Examples:
    # url(r'^$', 'versus.views.home', name='home'),
    # url(r'^versus/', include('versus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()


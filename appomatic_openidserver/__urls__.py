from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^openid/', include('openid_provider.urls')),
)

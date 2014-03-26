from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^openid/xrds/sso/logout/?', 'appomatic_openidserver.views.sso_logout'),
    (r'^openid/', include('openid_provider.urls')),
)

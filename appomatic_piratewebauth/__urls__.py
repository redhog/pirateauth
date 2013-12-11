from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^login/done/?', 'appomatic_piratewebauth.views.login_done'),
    (r'^login/?', 'appomatic_piratewebauth.views.login'),
)

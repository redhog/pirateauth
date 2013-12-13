import django.http
import urllib
import urllib2
import django.contrib.auth
import lxml.etree
import django.contrib.auth.models
from django.conf import settings

def login(request):
    next = request.GET.get("next", "/")

    if request.user.is_authenticated():
        return django.http.HttpResponseRedirect(next)

    request.session['piratewebauth_next'] = next

    return django.http.HttpResponseRedirect(settings.PIRATEWEB_REDIRECT_URL % {
            "next": urllib.quote_plus("http://" + django.contrib.sites.models.get_current_site(request).domain + django.core.urlresolvers.reverse("appomatic_piratewebauth.views.login_done"))})

def login_done(request):
    next = request.session['piratewebauth_next']

    print request.GET

    if request.GET.get("result", "failure") != "success" or "ticket" not in request.GET:
        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse("appomatic_piratewebauth.views.login") + "?next=" + next)

    ticket = request.GET["ticket"]

    txt = content = urllib2.urlopen(settings.PIRATEWEB_VALIDATE_URL % {"ticket": ticket}, "GET").read()
    content = lxml.etree.fromstring(content)
    
    if not content.tag == "VALID":
        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse("appomatic_piratewebauth.views.login") + "?next=" + next)

    userdata = dict((item.tag.lower(), item.text) for item in content.xpath("//VALID/USER/*"))
    userdata['geographiesforperson'] = content.xpath("//VALID/USER/GEOGRAPHIESFORPERSON//*/@name")
    userdata['memberships'] = content.xpath("//VALID/USER/MEMBERSHIPS/*/@name")

    userdata['memberships'] = ['org--' + name for name in userdata['memberships']]

    userdata['geographiesforperson'].reverse()
    geopath = ['geo']
    for item in userdata.pop('geographiesforperson'):
        geopath.append(item)
        userdata['memberships'].append('--'.join(geopath))


    existingusers = django.contrib.auth.models.User.objects.filter(username = userdata['openidhandle'])
    if existingusers:
        user = existingusers[0]
    else:
        user = django.contrib.auth.models.User()

    user.username = userdata.pop('openidhandle')
    user.email = userdata.pop('email')
    user.first_name = userdata.pop('givenname')
    user.last_name = userdata.pop('sn')

    user.save()

    groups = []
    for groupname in userdata.pop('memberships'):
        existinggroups = django.contrib.auth.models.Group.objects.filter(name = groupname)
        if existinggroups:
            groups.extend(existinggroups)
        else:
            group = django.contrib.auth.models.Group(name = groupname)
            group.save()
            groups.append(group)
    user.groups.clear()
    user.groups.add(*groups)

    if not existingusers:
        user.openid_set.create(openid=user.username)

    openid = user.openid_set.all()[0]
    openid.axdatas.all().delete()
    openidmap = {
        'phone': 'http://openid.net/schema/contact/phone/default'
        }
    for key, value in userdata.iteritems():
        if key in openidmap:
            openid.axdatas.create(key = openidmap[key], value=value)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    django.contrib.auth.login(request, user)

    return django.http.HttpResponseRedirect(urllib.unquote_plus(next))

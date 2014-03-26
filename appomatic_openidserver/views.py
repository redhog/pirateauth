import django.contrib.auth

def sso_logout(request):
    django.contrib.auth.logout(request)
    return django.shortcuts.redirect(request.GET['logout_redirect'])

OPENID_PROVIDER_STORE = 'django_openid_auth.store.DjangoOpenIDStore'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
OPENID_FORCE_AUTH = True
OPENID_AUTHORIZE_DATA = True
OPENID_PROVIDER_SREG_DATA_CALLBACK = 'appomatic_openidserver.callbacks.get_sreg_data'
OPENID_PROVIDER_AX_EXTENSION = True
OPENID_PROVIDER_AX_DATA_CALLBACK = 'appomatic_openidserver.callbacks.get_ax_data'

import django.contrib.auth.models
import fcdjangoutils.fields
import django.contrib.admin

class User(django.contrib.auth.models.User):
    info = fcdjangoutils.fields.JsonField()

class UserAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_display_links = list_display
    search_fields = list_display + ('info',)
django.contrib.admin.site.register(User, UserAdmin)

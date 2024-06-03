from django.contrib import admin
from django.contrib.auth.models import Group

from apps.models import Users, Subject


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)

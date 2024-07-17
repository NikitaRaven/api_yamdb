from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'role')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role']
    list_filter = ['role']


admin.site.register(CustomUser, CustomUserAdmin)

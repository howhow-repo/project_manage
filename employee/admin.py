# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User, Department
from .forms import GroupAdminForm


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'nickname', 'department', 'phone_number', 'is_accept')
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Additional Info',
            {
                'fields': (
                    'nickname',
                    'department',
                    'is_accept'
                )
            }
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'nickname', 'password1', 'password2', 'department', 'is_accept')}),
    )


class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, CustomUserAdmin)

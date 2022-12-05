# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'department', 'phone_number', 'is_accept')
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Additional Info',
            {
                'fields': (
                    'nickname',
                    'department',
                    'location',
                    'is_accept'
                )
            }
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'nickname', 'password1', 'password2', 'department', 'is_accept')}),
    )


admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, CustomUserAdmin)

# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from employee.models import Department, User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "first_name",
                "class": "form-control"
            }
        ))

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "last_name",
                "class": "form-control"
            }
        ))

    nickname = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "nickname",
                "class": "form-control"
            }
        ))

    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "phone_number",
                "class": "form-control"
            }
        ))

    department = forms.ModelChoiceField(
        required=False,
        queryset=Department.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "department",
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'nickname', 'phone_number', 'password1', 'password2', 'department')


class DeleteUserForm(forms.Form):
    confirm = forms.CharField(widget=forms.HiddenInput(), initial='yes')


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance

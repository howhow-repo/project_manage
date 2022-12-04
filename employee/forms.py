# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from employee.models import Department, BranchLocation


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
        required=True,
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
        required=False,
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

    location = forms.ModelChoiceField(
        required=False,
        queryset=BranchLocation.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "location",
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
        fields = ('username', 'email', 'phone_number', 'password1', 'password2', 'location', 'department')


class DeleteUserForm(forms.Form):
    confirm = forms.CharField(widget=forms.HiddenInput(), initial='yes')

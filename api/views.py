# -*- encoding: utf-8 -*-
import logging
import os

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.authentication.forms import LoginForm
from .forms import CheckLoginForm

logger = logging.getLogger(__name__)


class CheckServerHealth(APIView):
    accept_keywords = ['app', 'cooper']
    parser_classes = (JSONParser,)
    permission_classes = [permissions.AllowAny]
    """
        For getting csrf token in cookie.
        For checking server is alive.
    """

    @swagger_auto_schema(
        operation_summary='Use it as ping.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'I_AM': openapi.Schema(type=openapi.TYPE_STRING, description='Please enter who you are.'),
            }
        )
    )
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.data.get('I_AM') and str.lower(request.data.get('I_AM')) in self.accept_keywords:
            healthy_msg = {
                'msg': 'I am alive!',
                'errCode': 0
            }
            return JsonResponse(healthy_msg)
        return HttpResponseForbidden()


class Login(APIView):
    """
        login.
    """

    parser_classes = (FormParser,)

    @swagger_auto_schema(
        operation_summary='Use it to login.',
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING,
                              description='Please enter who you are.'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING,
                              description='Please enter your password.'),
        ]
    )
    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                r = login(request, user)
                return JsonResponse({
                    'msg': 'success',
                })
            else:
                msg = 'Invalid credentials'
        else:
            print(form.errors)
            msg = f'Error validating the form.'
        return JsonResponse({'msg': msg})


class Logout(APIView):
    """
    Logout
    """

    @swagger_auto_schema(
        operation_summary='Use it to logout.',
    )
    def post(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': 'you are not login.'}, status=403)


class AmILogin(APIView):
    parser_classes = (FormParser,)

    @swagger_auto_schema(
        operation_summary='Use it to Check Auth.',
    )
    def post(self, request):
        form = CheckLoginForm(request.POST or None)
        if request.user.is_authenticated:
            return JsonResponse({'you_are': 'Login'})
        elif form.is_valid():
            return JsonResponse({'you_are': 'form is correct, but request is not authenticated'})
        else:
            return JsonResponse({'you_are': 'not authenticated'})

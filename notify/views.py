from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def add_schedule_notify(request):
    context = {'segment': 'notify'}
    return render(request, 'add_schedule_notify.html', context)


from django.shortcuts import render


def add_schedule_notify(request):
    context = {'segment': 'notify'}
    return render(request, 'add_schedule_notify.html', context)


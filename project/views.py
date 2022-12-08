from django.db import models
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from customer.models import Customer
from customer.views import fill_form_initial_with_org_data
from .forms import ProjectForm
from .models import Project, DailyReport, DailyReportImages


def add_creator_and_customer(model_obj, customer, creater):
    model_obj.customer = customer
    model_obj.creator = creater
    return model_obj


def add_project(request, customer_name):
    try:
        customer = Customer.objects.get(name=customer_name)
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            model_obj = form.save(commit=False)
            model_obj = add_creator_and_customer(model_obj, customer, request.user)
            model_obj.save()
            context['Msg'] = 'Success'
            customer.editor = request.user
            customer.update_time = timezone.now()
            customer.save()
            return HttpResponseRedirect(reverse('customer_detail', kwargs={'cust_name': customer_name}))
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = ProjectForm()
    form.fields['customer'].initial = customer
    context.update({'form': form, 'customer': customer})
    return render(request, 'add_project.html', context)


def project_detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    if request.method == "POST":
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.editor = request.user
            project.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = ProjectForm()
    form = fill_form_initial_with_org_data(project, form)
    context.update({
        'form': form,
        "project": project,
        "daily_reports": DailyReport.objects.filter(project=project).order_by('-update_time')
    })
    return render(request, 'project_detail.html', context)



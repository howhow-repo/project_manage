from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from customer.models import Customer
from customer.views import fill_form_initial_with_org_data
from .forms import ProjectForm, DailyReportForm, DailyReportPhotoForm
from .models import Project, DailyReport, DailyReportPhoto


def add_creator_and_customer(model_obj, customer, creater):
    model_obj.customer = customer
    model_obj.creator = creater
    model_obj.editor = creater
    return model_obj


def count_photos(report_id):
    photo_sets = DailyReportPhoto.objects.filter(report=report_id)
    if not len(photo_sets):
        return 0

    counter = 0
    for photo_set in photo_sets:
        for k in photo_set.__dict__.keys():
            if 'photo' in k and getattr(photo_set, k):
                counter += 1
    return counter


def get_page(request):
    try:
        return int(request.GET['page'])
    except Exception:
        return 1


def get_num_of_page(request):
    try:
        return int(request.GET['data_num'])
    except Exception:
        return 50


@login_required(login_url="/login/")
def list_projects(request):
    data_num = get_num_of_page(request)
    page = get_page(request)

    projects = Project.objects.all().order_by('-update_time')
    query_set_len = len(projects)
    paginator = Paginator(projects, data_num)
    projects = paginator.get_page(page)
    
    context = {
        'segment': 'project',
        'projects': projects,
        'data_num': data_num,
        'query_set_len': query_set_len
    }
    return render(request, 'list_projects.html', context)


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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

    daily_reports = DailyReport.objects.filter(project=project).order_by('-update_time')
    num_of_photo = [range(count_photos(r.id)) for r in daily_reports]
    daily_reports = zip(daily_reports, num_of_photo)

    context.update({
        'form': form,
        "project": project,
        "daily_reports": daily_reports,
        "calendar_template_link": project.google_calendar_event(request)
    })
    return render(request, 'project_detail.html', context)


@login_required(login_url="/login/")
def add_daily_report(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    if request.method == "POST":
        report_form = DailyReportForm(data=request.POST)
        photo_form = DailyReportPhotoForm(data=request.POST, files=request.FILES)
        if report_form.is_valid() and photo_form.is_valid():
            report_instance = report_form.save(commit=False)
            report_instance.creator = request.user
            report_instance.save()

            images_instance = photo_form.save(commit=False)
            images_instance.report = report_instance
            images_instance.save()

            project.update_time = timezone.now()
            project.save()
            project.customer.update_time = timezone.now()
            project.customer.save()

            context['Msg'] = 'Success'
            return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id': project.id}))
        else:
            context['errMsg'] = 'Form is not valid'

    else:
        report_form = DailyReportForm()
        report_form.fields['project'].initial = project
        photo_form = DailyReportPhotoForm()
        photo_form.fields['report'].initial = project

    context.update({
        'report_form': report_form,
        'photo_form': photo_form,
        "project": project,
    })
    return render(request, 'add_daily_report.html', context)

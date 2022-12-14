from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from customer.models import Customer, FavoriteCustomer
from customer.views import fill_form_initial_with_org_data
from notify.lib.notify_followers import notify_customer_followers, notify_project_followers
from .forms import ProjectForm, DailyReportForm, DailyReportPhotoForm, FavoriteProjectForm
from .models import Project, DailyReport, DailyReportPhoto, FavoriteProject
from lib.translate_table import TranslateTable


def get_model_or_none(model, query_dict):
    try:
        return model.objects.get(**query_dict)
    except models.ObjectDoesNotExist:
        return None


def send_add_project_to_followers(request, new_project):
    s = f"{request.user.nickname}建立新專案：\n" \
        f"({new_project.customer.name})[專案]{new_project.title}/{new_project.type}\n"
    notify_customer_followers(new_project.customer, s)


def send_change_message_to_followers(request, updated_form):
    updated_project = updated_form.instance
    s = f"{request.user.nickname} 更新了 \n" \
        f"[專案]{updated_project.title}/{updated_project.type}({updated_project.customer.name})\n" \
        f"更新欄位：{[TranslateTable[field] for field in updated_form.changed_data]}"
    notify_project_followers(updated_project, s)


def send_add_report_message_to_followers(request, report):
    s = f"{request.user.nickname} 建立了紀錄: \n " \
        f"[{report.project.customer.name}]{report.project.title}/{report.project.type}\n" \
        f"---\n" \
        f"{report.note}\n" \
        f"---\n" \
        f"{report.project.create_detail_link(request)}"
    notify_project_followers(report.project, s)


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


def save_new_project(request, customer):
    form = ProjectForm(data=request.POST)
    if form.is_valid():
        new_project = form.save(commit=False)
        new_project.customer = customer
        new_project.creator = request.user
        new_project.editor = request.user
        new_project.save()
        customer.editor = request.user
        customer.update_time = timezone.now()
        customer.save()
        return new_project
    return None


def update_project():
    pass


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
    queryset_len = len(projects)
    paginator = Paginator(projects, data_num)
    projects = paginator.get_page(page)
    
    context = {
        'segment': 'project',
        'projects': projects,
        'data_num': data_num,
        'query_set_len': queryset_len
    }
    return render(request, 'list_projects.html', context)


@login_required(login_url="/login/")
def add_project(request, customer_name):
    customer = get_model_or_none(Customer, {'name': customer_name})
    if not customer:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        new_project = save_new_project(request, customer)
        if new_project:
            context['Msg'] = 'Success'
            send_add_project_to_followers(request, new_project)
            return HttpResponseRedirect(reverse('customer_detail', kwargs={'cust_name': customer_name}))
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = ProjectForm()
    form.fields['customer'].initial = customer
    form.fields['address'].initial = customer.address
    context.update({'form': form, 'customer': customer})
    return render(request, 'add_project.html', context)


@login_required(login_url="/login/")
def project_detail(request, project_id):
    project = get_model_or_none(Project, {'id': project_id})
    if not project:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    if request.method == "POST":
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            updated_project = form.save(commit=False)
            updated_project.editor = request.user
            updated_project.save()
            context['Msg'] = 'Success'

            send_change_message_to_followers(request, form)

            form = fill_form_initial_with_org_data(updated_project, form)
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = ProjectForm()
        form = fill_form_initial_with_org_data(project, form)

    add_favorite_form = FavoriteProjectForm()
    add_favorite_form.set_initial(request.user.id, project_id)

    daily_reports = DailyReport.objects.filter(project=project).order_by('-update_time')
    num_of_photo = [range(count_photos(r.id)) for r in daily_reports]
    daily_reports = zip(daily_reports, num_of_photo)

    context.update({
        'form': form,
        "project": project,
        "daily_reports": daily_reports,
        "calendar_template_link": project.google_calendar_event(request),
        "add_favorite_form": add_favorite_form,
        "is_favorite": FavoriteProject.objects.filter(user=request.user, project=project).exists()
    })
    return render(request, 'project_detail.html', context)


@login_required(login_url="/login/")
def add_daily_report(request, project_id):
    project = get_model_or_none(Project, {'id': project_id})
    if not project:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    if request.method == "POST":
        report_form = DailyReportForm(data=request.POST)
        photo_form = DailyReportPhotoForm(data=request.POST, files=request.FILES)
        if report_form.is_valid() and photo_form.is_valid():
            # save report
            report_instance = report_form.save(commit=False)
            report_instance.creator = request.user
            report_instance.save()

            # save photo
            images_instance = photo_form.save(commit=False)
            images_instance.report = report_instance
            images_instance.save()

            # update project time
            project.update_time = timezone.now()
            project.save()

            # send notify
            send_add_report_message_to_followers(request, report_instance)

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

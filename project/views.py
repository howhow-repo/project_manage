from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from threading import Thread
from customer.models import Customer
from lib import get_model_or_none
from .forms import ProjectForm, DailyReportForm, DailyReportPhotoForm, FavoriteProjectForm
from .lib.project_lib import save_new_project_or_none, send_add_project_msg_to_followers, send_owner_notify, \
    send_change_message_to_followers, send_add_report_message_to_followers, count_photos, get_num_of_page, get_page
from .models import Project, DailyReport, FavoriteProject


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
def add_project(request, customer_id):
    customer = get_model_or_none(Customer, {'id': customer_id})
    if not customer:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    # Do POST
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        new_project = save_new_project_or_none(request, customer)
        if new_project:
            context['Msg'] = 'Success'
            Thread(target=send_add_project_msg_to_followers, args=(request, new_project)).start()
            if new_project.owner:
                Thread(target=send_owner_notify, args=(request, new_project)).start()
            # everything ok
            return HttpResponseRedirect(reverse('customer_detail', kwargs={'cust_id': customer_id}))
        else:
            context['errMsg'] = 'Form is not valid'

    # Do GET
    else:
        form = ProjectForm()

    form.fields['customer'].initial = customer
    form.fields['address'].initial = customer.address
    form.fields['dispatch_date'].initial = timezone.now()
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

            Thread(target=send_change_message_to_followers, args=(request, form)).start()

            form = ProjectForm(data=request.POST, instance=updated_project)
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = ProjectForm(instance=project)

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
            Thread(target=send_add_report_message_to_followers, args=(request, report_instance)).start()

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

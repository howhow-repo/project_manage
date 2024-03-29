from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from customer.forms import FavoriteCustomerForm
from customer.models import Customer, FavoriteCustomer
from project.models import Project, FavoriteProject
from project.forms import FavoriteProjectForm
from .forms import UserProfileEdit


def is_in_project_favorite(user, project):
    if FavoriteProject.objects.filter(user=user, project=project).exists():
        return True
    return False


def is_in_customer_favorite(user, customer):
    if FavoriteCustomer.objects.filter(user=user, customer=customer).exists():
        return True
    return False


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    if request.method == 'POST':
        form = UserProfileEdit(data=request.POST, instance=request.user)
        if form.is_valid() and form.changed_data:
            user = form.save(commit=False)
            user.save()
            context['Msg'] = 'Success'
            user.send_line_notify(f"個人資訊已上傳: {form.changed_data}")
        elif not form.is_valid():
            context['errMsg'] = form.errors.as_data()

    form = UserProfileEdit(instance=request.user)

    context['form'] = form
    context['favorite_projects'] = FavoriteProject.objects.filter(user=request.user).order_by('-project__update_time')
    context['favorite_customers'] = FavoriteCustomer.objects.filter(user=request.user).order_by('-customer__update_time')
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            user.send_line_notify("密碼更改成功!")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


@login_required(login_url="/login/")
@require_http_methods(["POST"])
def add_favorite_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Exception:
        return HttpResponseNotFound()

    form = FavoriteProjectForm(request.POST)
    if form.is_valid():
        if not is_in_project_favorite(request.user, project):
            favorite_project = form.save(commit=False)
            favorite_project.project = project
            favorite_project.user = request.user
            favorite_project.save()

        else:
            return HttpResponse("You've added already.")
    return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id': project.id}))


@login_required(login_url="/login/")
@require_http_methods(["POST"])
def rm_favorite_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Exception:
        return HttpResponseNotFound()

    form = FavoriteProjectForm(request.POST)
    if form.is_valid():
        if is_in_project_favorite(request.user, project):
            f_project = FavoriteProject.objects.get(user=request.user, project=project)
            f_project.delete()
        else:
            return HttpResponse("it is not in you 關注．")
    return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id': project.id}))


@login_required(login_url="/login/")
@require_http_methods(["POST"])
def add_favorite_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Exception:
        return HttpResponseNotFound()
    #
    form = FavoriteCustomerForm(request.POST)
    if form.is_valid():
        if not is_in_customer_favorite(request.user, customer):
            favorite_customer = form.save(commit=False)
            favorite_customer.customer = customer
            favorite_customer.user = request.user
            favorite_customer.save()
        else:
            return HttpResponse("You've added already.")
    return HttpResponseRedirect(reverse('customer_detail', kwargs={'cust_id': customer.id}))


@login_required(login_url="/login/")
@require_http_methods(["POST"])
def rm_favorite_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Exception:
        return HttpResponseNotFound()

    form = FavoriteCustomerForm(request.POST)

    if form.is_valid():
        if is_in_customer_favorite(request.user, customer):
            f_customer = FavoriteCustomer.objects.get(user=request.user, customer=customer)
            f_customer.delete()
        else:
            return HttpResponse("it is not in you 關注．")
    return HttpResponseRedirect(reverse('customer_detail', kwargs={'cust_id': customer.id}))

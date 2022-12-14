from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from lib.fill_form_initial_with_org_data import fill_form_initial_with_org_data
from lib.translate_table import TranslateTable
from notify.lib.notify_followers import notify_customer_followers
from project.models import Project
from project.views import get_model_or_none
from .models import Customer, FavoriteCustomer
from .forms import CustomerForm


def send_change_message_to_followers(request, updated_form):
    updated_customer = updated_form.instance
    s = f"{request.user.nickname} 更新了 \n" \
        f"[客戶]{updated_customer.name}({updated_customer.status})\n" \
        f"更新欄位：{[TranslateTable[field] for field in updated_form.changed_data]}"
    notify_customer_followers(updated_customer, s)


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
def list_customers(request):
    data_num = get_num_of_page(request)
    page = get_page(request)

    customers = Customer.objects.all().order_by('-update_time')
    query_set_len = len(customers)
    paginator = Paginator(customers, data_num)
    customers = paginator.get_page(page)
    context = {'customers': customers, 'data_num': data_num, 'query_set_len': query_set_len }
    return render(request, 'list_customers.html', context)


@login_required(login_url="/login/")
def add_customer(request):
    context = {'segment': 'customer'}
    if request.method == "POST":
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.editor = request.user
            obj.save()
            context['Msg'] = 'Success'
            return HttpResponseRedirect(reverse('list_customers'))
        else:
            context['errMsg'] = 'Form is not valid'
    context.update({'form': CustomerForm()})
    return render(request, 'add_customer.html', context)


@login_required(login_url="/login/")
def customer_detail(request, cust_name):
    customer = get_model_or_none(Customer, {'name': cust_name})
    if not customer:
        return HttpResponseNotFound()

    context = {'segment': 'customer'}
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.editor = request.user
            customer.save()
            context['Msg'] = 'Success'
            send_change_message_to_followers(request, form)
        else:
            context['errMsg'] = form.errors
    else:
        form = CustomerForm()

    form = fill_form_initial_with_org_data(customer, form)
    context.update({
        'form': form,
        'customer': customer,
        'projects': Project.objects.filter(customer=customer).order_by('-update_time'),
        'is_favorite': FavoriteCustomer.objects.filter(user=request.user, customer=customer).exists()
    })
    return render(request, 'customer_detail.html', context)

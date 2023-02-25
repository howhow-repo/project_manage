from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from threading import Thread

from project.models import Project
from lib import get_model_or_none
from .lib.customer_lib import get_num_of_page, get_page, send_change_message_to_followers, get_cel, get_filter, \
    get_keyword
from .models import Customer, FavoriteCustomer
from .forms import CustomerForm, PreAddCustomerForm, SearchCustomerForm


@login_required(login_url="/login/")
def list_customers(request):
    data_num = get_num_of_page(request)
    page = get_page(request)
    cus_filter = get_filter(request)  # ['name', 'cel', 'tel', 'address', 'type', 'status']
    keyword = get_keyword(request)
    if cus_filter and keyword:
        customers = Customer.objects.filter(**{f'{cus_filter}__icontains': keyword}).order_by('-update_time')
    else:
        customers = Customer.objects.all().order_by('-update_time')
    query_set_len = len(customers)
    paginator = Paginator(customers, data_num)
    customers = paginator.get_page(page)
    context = {'customers': customers, 'data_num': data_num, 'query_set_len': query_set_len, 'segment': 'customer'}
    if cus_filter and keyword:
        context.update({'filter': cus_filter, 'keyword': keyword})
    return render(request, 'list_customers.html', context)


@login_required(login_url="/login/")
def add_customer(request):
    context = {'segment': 'customer'}
    if request.method == "POST":
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.cel = customer.cel.replace(" ", "")
            customer.creator = request.user
            customer.editor = request.user
            customer.save()
            context['Msg'] = 'Success'
            return HttpResponseRedirect(reverse('list_customers'))
        else:
            context['errMsg'] = 'Form is not valid'
    cel = get_cel(request)
    form = CustomerForm(initial={'cel': cel})
    context.update({'form': form})
    return render(request, 'add_customer.html', context)


@login_required(login_url="/login/")
def pre_add_customer(request):
    context = {'segment': 'customer'}
    if request.method == "POST":
        form = PreAddCustomerForm(data=request.POST)
        if form.is_valid():
            cel = form.data.get('cel').replace(" ", "")
            customer = get_model_or_none(Customer, {'cel': cel})
            if not customer:
                return HttpResponseRedirect(reverse('add_customer')+f'?cel={cel}')
            elif customer:
                return HttpResponseRedirect(reverse('customer_detail', kwargs={'cust_id': customer.id}))

    context.update({'form': PreAddCustomerForm()})
    return render(request, 'pre_add_customer.html', context)


@login_required(login_url="/login/")
def customer_detail(request, cust_id):
    customer = get_model_or_none(Customer, {'id': cust_id})
    if not customer:
        return HttpResponseNotFound()

    context = {'segment': 'customer'}
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.cel = customer.cel.replace(" ", "")
            customer.editor = request.user
            customer.save()
            Thread(target=send_change_message_to_followers, args=(request, form)).start()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = form.errors

    form = CustomerForm(instance=customer)
    context.update({
        'form': form,
        'customer': customer,
        'projects': Project.objects.filter(customer=customer).order_by('-update_time'),
        'is_favorite': FavoriteCustomer.objects.filter(user=request.user, customer=customer).exists()
    })
    return render(request, 'customer_detail.html', context)


@login_required(login_url="/login/")
def search_customers(request):
    context = {'segment': 'customer'}
    if request.method == 'POST':
        form = SearchCustomerForm(data=request.POST)
        if form.is_valid():
            f = form.data['filter']
            k = form.data['keyword']
            return HttpResponseRedirect(reverse('list_customers') + f'?filter={f}&keyword={k}')

    context.update({'form': SearchCustomerForm()})
    return render(request, 'search_customers.html', context)
    
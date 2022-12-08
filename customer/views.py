from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from project.models import Project
from .models import Customer
from .forms import CustomerForm


def fill_form_initial_with_org_data(org_instance, form):
    for element in form.fields:
        db_data = getattr(org_instance, element)
        if db_data is not None or db_data != "":
            form.fields[element].initial = db_data
    return form


@login_required(login_url="/login/")
def list_customers(request):
    context = {'customers': Customer.objects.all().order_by('-update_time')}
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
    try:
        customer = Customer.objects.get(name=cust_name)
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()

    context = {'segment': 'customer'}
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.editor = request.user
            customer.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = form.errors
    else:
        form = CustomerForm()

    form = fill_form_initial_with_org_data(customer, form)
    context.update({
        'form': form,
        'customer': customer,
        'projects': Project.objects.filter(customer=customer)
    })
    return render(request, 'customer_detail.html', context)

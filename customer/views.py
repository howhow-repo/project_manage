from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

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
    context = {}
    if request.method == "POST":
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = 'Form is not valid'
    context = {'form': CustomerForm()}
    return render(request, 'add_customer.html', context)


@login_required(login_url="/login/")
def customer_detail(request, cust_name):
    customer = Customer.objects.get(name=cust_name)
    if not customer:
        return HttpResponseNotFound()

    context = {'segment': 'customer'}

    form = CustomerForm()
    if request.method == 'POST':
        update_form = CustomerForm(data=request.POST, instance=customer)
        if update_form.is_valid():
            obj = update_form.save(commit=False)
            obj.creator = request.user
            obj.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = update_form.errors
    form = fill_form_initial_with_org_data(Customer.objects.get(name=cust_name), form)

    context.update({
        'form': form,
        'customer': customer,
        'projects': Project.objects.filter(customer=customer)
    })
    return render(request, 'customer_detail.html', context)

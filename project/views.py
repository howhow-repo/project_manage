from django.http import HttpResponseNotFound
from django.shortcuts import render

from customer.models import Customer
from .forms import ProjectForm


def add_project(request, customer_name):
    customer = Customer.objects.get(name=customer_name)
    if not customer:
        return HttpResponseNotFound()

    context = {}
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.customer = customer
            obj.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = 'Form is not valid'
            print(form.errors.as_data())
    form = ProjectForm()
    form.fields['customer'].initial = customer
    context.update({'form': form, 'customer': customer})
    return render(request, 'add_project.html', context)

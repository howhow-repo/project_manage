from django.shortcuts import render

from customer.models import CustomerType, CustomerStatus
from material.models import MaterialType
from project.models import ProjectStatus, ProjectType
from quotation.models import BomStatus


def get_class_by_name(name, options):
    for cls in options:
        if cls.__name__ == name:
            return cls
    return None


# Create your views here.
def list_options(request):
    context = {'segment': 'option_settings'}
    options = ['CustomerType', 'CustomerStatus', 'MaterialType', 'ProjectStatus', 'ProjectType', 'BomStatus']
    options_ch = ['客戶類型', '客戶狀態', '料件類型', '專案狀態', '專案類型', '報價單狀態']
    context.update({'options': zip(options, options_ch)})
    return render(request, 'list_options.html', context)


def edit_choices(request, option_name):
    context = {'segment': 'option_settings'}
    options = [CustomerType, CustomerStatus, MaterialType, ProjectStatus, ProjectType, BomStatus]
    option = get_class_by_name(option_name, options)
    context.update({'choices': option.objects.all(), 'option_name': option_name})
    return render(request, 'edit_choices.html', context)


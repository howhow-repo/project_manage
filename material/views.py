from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from lib import get_model_or_none, fill_form_initial_with_org_data
from .models import Material
from .forms import MaterialForm


def list_materials(request):
    context = {'segment': 'material', 'materials': Material.objects.all()}
    return render(request, 'list_materials.html', context)


@login_required(login_url="/login/")
def add_material(request):
    context = {'segment': 'material'}
    if request.method == "POST":
        form = MaterialForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator, obj.editor = request.user, request.user
            obj.save()
            context['Msg'] = 'Success'
            return HttpResponseRedirect(reverse('list_materials'))
        else:
            context['errMsg'] = f'Form is not valid: {form.errors.as_data()}'
    else:
        form = MaterialForm()

    context.update({'form': form})
    return render(request, 'add_material.html', context)


@login_required(login_url="/login/")
def delete_material(request):
    pass  # TODO


@login_required(login_url="/login/")
def material_detail(request, material_name):
    material = get_model_or_none(Material, {'name': material_name})
    if not material:
        return HttpResponseNotFound()

    context = {'segment': 'material'}
    if request.method == 'POST':
        form = MaterialForm(data=request.POST, instance=material)
        if form.is_valid():
            material = form.save(commit=False)
            material.editor = request.user
            material.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = form.errors
    else:
        form = MaterialForm()
    form = fill_form_initial_with_org_data(material, form)
    context.update({
        'form': form,
        'material': material,
    })
    return render(request, 'material_detail.html', context)

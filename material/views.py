from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from lib import get_model_or_none, fill_form_initial_with_org_data, manager_required
from .models import Material, MaterialType
from .forms import MaterialForm, MaterialTypeForm, MaterialTypeDelForm


def list_materials(request):
    context = {'segment': 'material', 'materials': Material.objects.all()}
    return render(request, 'list_materials.html', context)


@manager_required
@login_required(login_url="/login/")
def material_type(request):
    context = {'segment': 'material'}
    if request.method == "POST":
        form = MaterialTypeForm(data=request.POST)
        if form.is_valid():
            form.save()

    form = MaterialTypeForm()
    material_type = MaterialType.objects.all()
    context.update({'form': form, 'material_type': material_type})
    return render(request, 'material_type.html', context)


@manager_required
@login_required(login_url="/login/")
def del_material_type(request, type_name):
    material_type = get_model_or_none(MaterialType, {'name': type_name})
    if request.method == "POST" and material_type:
        form = MaterialTypeDelForm(data=request.POST)
        if form.is_valid():
            try:
                material_type.delete()
            except ProtectedError:
                return HttpResponseBadRequest("分類使用中，無法刪除。")
    return HttpResponseRedirect(reverse('material_type'))


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

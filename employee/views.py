from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from lib import manager_required
from .forms import SignUpForm, DeleteUserForm
from index.forms import UserProfileEdit
from django.http import HttpResponseRedirect, HttpResponseServerError


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def view_all_users(request):
    context = {
        'manager': True,
        'segment': 'user_management',
        'users': []
    }
    User = get_user_model()
    users = User.objects.all()
    context['users'] = [u for u in users if u.username != request.user.username]
    return render(request, 'user_management.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_all_users')
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "create_user.html",
                  {
                      'manager': True,
                      'segment': 'user_management',
                      'form': form,
                      'msg': msg,
                      'success': success
                  })


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def edit_user(request, username):
    context = {'manager': True, 'segment': 'user_management', 'edit_user': username}
    User = get_user_model()
    user = User.objects.get(username=username)

    if request.method == "POST":
        update_form = UserProfileEdit(data=request.POST, instance=user)
        if update_form.is_valid():
            user = update_form.save(commit=False)
            user.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = 'Form is not valid'

    form = UserProfileEdit(instance=user)

    context['form'] = form
    return render(request, 'edit_user.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_user(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)

    if request.method == "POST":
        form = DeleteUserForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            try:
                user.delete()
            except ProtectedError:
                return HttpResponseServerError("ProtectedError")
            messages.success(request, "The user is deleted")
        return HttpResponseRedirect("/user_management")

    else:
        context = {'manager': True, 'segment': 'user_management', 'delete_user': username, 'form': DeleteUserForm()}
        return render(request, 'delete_user_confirm.html', context)

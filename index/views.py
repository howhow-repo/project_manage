from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileEdit


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    User = get_user_model()
    user = User.objects.get(username=request.user)
    form = UserProfileEdit()

    if request.method == 'POST':
        update_form = UserProfileEdit(data=request.POST, instance=request.user)
        if update_form.is_valid():
            user = update_form.save(commit=False)
            user.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = update_form.errors.as_data()

    for element in form.fields:
        data_from_user = getattr(user, element)
        if data_from_user is not None or data_from_user != "":
            form.fields[element].initial = data_from_user

    context['form'] = form
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

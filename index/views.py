from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from customer.views import fill_form_initial_with_org_data
from .forms import UserProfileEdit


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    User = get_user_model()
    user = User.objects.get(username=request.user)

    if request.method == 'POST':
        form = UserProfileEdit(data=request.POST, instance=request.user)
        if form.is_valid() and form.changed_data:
            user = form.save(commit=False)
            user.save()
            # update_session_auth_hash(request, user)  # Important!
            context['Msg'] = 'Success'
            user.send_line_notify(f"個人資訊已上傳: {form.changed_data}")
        elif not form.is_valid():
            context['errMsg'] = form.errors.as_data()
    else:
        form = UserProfileEdit()
    form = fill_form_initial_with_org_data(user, form)

    context['form'] = form
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            user.send_line_notify("密碼更改成功!")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)


    return render(request, 'change_password.html', {'form': form})

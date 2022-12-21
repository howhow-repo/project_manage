from django.http import HttpResponseForbidden
from django.template import loader


def manager_required(func):  # use as decorator
    def wrapper(request, *args, **kwargs):
        if request.user.department and request.user.department.name == '管理':
            return func(request, *args, **kwargs)
        else:
            html_template = loader.get_template('home/page-403.html')
            return HttpResponseForbidden(HttpResponse(html_template.render({}, request)))

    return wrapper

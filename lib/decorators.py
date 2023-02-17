from django.http import HttpResponseForbidden, HttpResponse
from django.template import loader


def manager_only(func):  # use as decorator
    def wrapper(request, *args, **kwargs):
        if request.user.department.name == '管理':
            return func(request, *args, **kwargs)
        else:
            html_template = loader.get_template('home/page-403.html')
            return HttpResponseForbidden(HttpResponse(html_template.render({}, request)))

    return wrapper


def baned_department(not_allow_depts: list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.department and request.user.department.name in not_allow_depts:
                html_template = loader.get_template('home/page-403.html')
                return HttpResponseForbidden(HttpResponse(html_template.render({}, request)))
            else:
                return func(request, *args, **kwargs)

        return wrapper
    return decorator


def allow_department(allow_depts: list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.department and request.user.department.name in allow_depts:
                return func(request, *args, **kwargs)
            else:
                html_template = loader.get_template('home/page-403.html')
                return HttpResponseForbidden(HttpResponse(html_template.render({}, request)))
        return wrapper
    return decorator

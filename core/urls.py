# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from customer.models import CustomerType, CaseStatus
from materials.models import Material, MaterialType

schema_view = get_schema_view(
    openapi.Info(
        title="Restful API",
        default_version='v1',
        description=r"api base url start with 'http://\<host\>:\<port\>/api/....'" +
                    "\n"
                    r"ex: http://\<host\>:\<port\>/api/CheckServerHealth",
    ),
    public=True,
    # permission_classes=[permissions.IsAuthenticated],
    permission_classes=[permissions.AllowAny],
)

try:
    Group.objects.get_or_create(name='manager')
    Group.objects.get_or_create(name='normal')
    CustomerType.objects.get_or_create(name='normal')
    CaseStatus.objects.get_or_create(name='來電詢問')
    CaseStatus.objects.get_or_create(name='待報價')
    CaseStatus.objects.get_or_create(name='報價完成')
    CaseStatus.objects.get_or_create(name='待出工')
    CaseStatus.objects.get_or_create(name='待收款')
    CaseStatus.objects.get_or_create(name='收款結束')
    Material.objects.get_or_create(
        name='人工', type=MaterialType.objects.get_or_create(name='人力'),
        unit='日', unit_price=1, note=None, creator=None
    )
except Exception:
    pass


urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    path("", include("index.urls")),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/", include("api.urls")),
    path("user_management/", include("employee.urls")),
    path("resource/", include("doc_handle.urls")),
    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("demo/", include("apps.demo.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

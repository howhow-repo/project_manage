# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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

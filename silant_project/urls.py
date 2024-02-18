from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Документация API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service_book.urls')),
    path('accounts/', include('allauth.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

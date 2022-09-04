from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce Fashion Brand API",
        default_version='v1',
        description='Rest API for Boisterus',
        contact=openapi.Contact(email="admin@gmail.com"), 
    ),
    public=True,
    permission_classes=[AllowAny]
    )

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('paystack/', include('paystack.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

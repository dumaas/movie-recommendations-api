from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_spectacular.views import SpectacularSwaggerView
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('my-admin-secret-portal/', admin.site.urls),

    # API
    path('endpoints/', include('endpoints.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('rest_framework.urls')),

    # dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration', include('dj_rest_auth.registration.urls')),

    # swagger documentation
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

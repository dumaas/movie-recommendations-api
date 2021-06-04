from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="API for generating movie recommendations and storing user data. Created by Christian Gonzalez.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="christiangonzalezblack@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

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
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

"""TAX INNOVATION URL Configuration"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include([  # noqa DJ05
        path('', include(('taxinnovation.apps.users.urls', 'users'), namespace='users')),
        path('catalogs/', include(('taxinnovation.apps.catalogs.urls', 'catalogs'), namespace='catalogs')),
        path('listo/', include(('taxinnovation.apps.listo_api.urls', 'listo_api'), namespace='listo_api'))

    ]))] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # OpenAPI
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
    
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),  # noqa DJ05
        ]


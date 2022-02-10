"""Users URLs."""

from django.urls import path, include


from rest_framework.routers import DefaultRouter

from taxinnovation.apps.catalogs.views import PostalCodeCatalogViewSet, NirUploadView, PhoneRulesCatalogViewSet, SerieRulesCatalogViewSet, RangeRulesCatalogViewSet


router = DefaultRouter()
router.register(r'postal-codes', PostalCodeCatalogViewSet, basename='postal-codes')
router.register(r'upload-nir-csv', NirUploadView, basename='upload-nir-csv')
router.register(r'nir-rules', PhoneRulesCatalogViewSet, basename='nir-rules')
router.register(r'serie-rules', SerieRulesCatalogViewSet, basename='serie-rules')
router.register(r'range-rules', RangeRulesCatalogViewSet, basename='range-rules')


urlpatterns = [
    path('', include((router.urls, 'catalogs'), namespace='catalogs')),
]

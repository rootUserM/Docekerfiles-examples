from django.contrib import admin

from taxinnovation.apps.catalogs.models import PostalCodeCatalog


@admin.register(PostalCodeCatalog)
class PostalCodeCatalogModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'postal_code',
        'settlement',
        'municipality',
        'city',
        'estate'
    )
    list_display_links = (
        'id',
        'postal_code'
    )
    search_fields = ('postal_code', )

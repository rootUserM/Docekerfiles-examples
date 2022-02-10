"""Addresses serializers."""

# Django REST Framework
from rest_framework import serializers

from taxinnovation.apps.catalogs.models.addresses import PostalCodeCatalog
from taxinnovation.apps.catalogs.models.phone_rules import NirRulesCatalog, SeriesRulesCatalog, PhoneRulesCatalog


class PostalCodeCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalCodeCatalog
        fields = (
            'id',
            'postal_code',
            'settlement',
            'municipality',
            'city',
            'estate',
        )


class NirRulesCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NirRulesCatalog
        fields = '__all__' 


class SerieRulesCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesRulesCatalog
        fields = '__all__' 


class RangeRulesCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneRulesCatalog
        fields = '__all__' 
        
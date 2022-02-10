import csv
import io
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets, status
from rest_framework import views
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Models
from taxinnovation.apps.catalogs.models import PostalCodeCatalog, NirRulesCatalog, SeriesRulesCatalog, PhoneRulesCatalog

# Serializers
from taxinnovation.apps.catalogs.serializers.addresses import PostalCodeCatalogSerializer, NirRulesCatalogSerializer, SerieRulesCatalogSerializer, RangeRulesCatalogSerializer


class PostalCodeCatalogViewSet(viewsets.ModelViewSet):
    queryset = PostalCodeCatalog.objects.all()
    serializer_class = PostalCodeCatalogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['postal_code']


class PhoneRulesCatalogViewSet(viewsets.ModelViewSet):
    queryset = NirRulesCatalog.objects.all()
    serializer_class = NirRulesCatalogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nir']

class SerieRulesCatalogViewSet(viewsets.ModelViewSet):
    queryset = SeriesRulesCatalog.objects.all()
    serializer_class = SerieRulesCatalogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nir_serie']

class RangeRulesCatalogViewSet(viewsets.ModelViewSet):
    queryset = PhoneRulesCatalog.objects.all()
    serializer_class = RangeRulesCatalogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nir_serie']


class NirUploadView(viewsets.GenericViewSet):
    """ Clase para subir csv con reglas de nirs. """
    @action(detail=False, methods=['post'], url_path='upload')
    def phone_upload(self, request):
        csv_file = request.FILES['file']

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        nir_repetidos = []
        nir_objects = []
        series_rules_catalog = []
        nir_serie_repetidos = []
        length_rules_catalog = []

        for column in csv.reader(io_string, delimiter=';', quotechar='|'):
            if column[7] not in nir_repetidos:
                nir_repetidos.append(column[7])
                nir_objects.append(
                    NirRulesCatalog(nir=column[7])
                )

            if (column[7] + column[8]) not in nir_serie_repetidos :
                nir_serie_repetidos.append(column[7] + column[8])
                series_rules_catalog.append(
                    SeriesRulesCatalog(
                        nir_id=column[7],
                        nir_serie=column[7] + column[8]
                    )
                )

            if column[12] == "MOVIL":
                length_rules_catalog.append(
                    PhoneRulesCatalog(
                        initial_number = column[9],
                        final_number = column[10],
                        nir_serie_id = column[7] + column[8],
                        kind_of_network = "MO",
                    )
               )
            elif column[12] == "FIJO":
                length_rules_catalog.append(
                    PhoneRulesCatalog(
                        initial_number = column[9],
                        final_number = column[10],
                        nir_serie_id = column[7] + column[8],
                        kind_of_network = "FI",
                    )
               )

        # Aplicando cambios a la base de datos
        NirRulesCatalog.objects.bulk_create(nir_objects)
        SeriesRulesCatalog.objects.bulk_create(series_rules_catalog)
        PhoneRulesCatalog.objects.bulk_create(length_rules_catalog)

        return Response(status=status.HTTP_201_CREATED)

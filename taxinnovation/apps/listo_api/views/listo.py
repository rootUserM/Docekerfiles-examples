from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.db import connection
from taxinnovation.apps.users.models import User, UserAddress, UserProfile
from taxinnovation.apps.users.permissions.users import isCompanyAdmin, IsAccountOwner, IsProfileOwner
from taxinnovation.apps.users.serializers.users import UserModelSerializer, UserProfileModelSerializer, UserTemporalMediaModelSerializer, TemporalMigrationToUserSerializer
from taxinnovation.apps.users.serializers.contact_user import UserAddressModelSerializer
from taxinnovation.apps.listo_api.models import Facturas, DireccionLegal, Lista69b, DeclaracionesDiots, OpinionCumplimiento, Declaraciones, Diots, Detalle_Declaracion_Declaracion, Detalle_Factura
from taxinnovation.apps.listo_api.serializers import InformacionModelSerializer

import json
import requests
from listoapi import ListoApi
from django.db.models import Q
from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend


def detalleFactura(user_id, id_factura, token_listo):

    url = 'https://listo.mx/api/invoices/'+str(id_factura)+''

    payload = {}
    headers = {
        'Authorization': 'Token '+token_listo+''
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp_dict = json.loads(response.text)

    queryset = Detalle_Factura(users_detalle_factura_id=user_id,
                               canceled_on=resp_dict['canceled_on'],
                               category_id=resp_dict['category_id'],
                               currency=resp_dict['currency'],
                               customer_id=resp_dict['customer_id'],
                               customer_rfc_id=resp_dict['customer_rfc_id'],
                               discounts=resp_dict['discounts'],
                               discounts_mxn=resp_dict['discounts_mxn'],
                               documents=resp_dict['documents'],
                               due_on=resp_dict['due_on'],
                               folio=resp_dict['folio'],
                               invoice_id=resp_dict['id'],
                               is_income=resp_dict['is_income'],
                               is_payroll=resp_dict['is_payroll'],
                               issued_on=getDate(resp_dict['issued_on']),
                               lineitems=resp_dict['lineitems'],
                               issuer_rfc=resp_dict['issuer_rfc'],
                               modified_on=resp_dict['modified_on'],
                               payer_rfc=resp_dict['payer_rfc'],
                               payroll_data_display=resp_dict['payroll_data_display'],
                               subtotal=resp_dict['subtotal'],
                               subtotal_mxn=resp_dict['subtotal_mxn'],
                               taxes=resp_dict['taxes'],
                               total=resp_dict['total'],
                               total_mxn=resp_dict['total_mxn'],
                               total_paid=resp_dict['total_paid'],
                               total_paid_mxn=resp_dict['total_paid_mxn'],
                               total_supplier_paid=resp_dict['total_supplier_paid'],
                               total_supplier_paid_mxn=resp_dict['total_supplier_paid_mxn'],
                               uuid=resp_dict['uuid'],
                               payment_method=resp_dict['payment_method'],
                               issuer_regime=resp_dict['issuer_regime'],
                               intended_use=resp_dict['intended_use'],
                               json_invoice_detail=resp_dict)
    queryset.save()


def getTaxes(taxes):
    x = 0
    for item in taxes:
        return taxes[x]['payable_due']
        x = x+1


def getDate(date):
    return date[0:10]


def detalleDeclaraciones(user_id, id_declaracion, token_listo):

    url = 'https://listo.mx/api/filings/filings/'+str(id_declaracion)+''

    payload = {}
    headers = {
        'Authorization': 'Token '+token_listo+''
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp_dict = json.loads(response.text)
    queryset = Detalle_Declaracion_Declaracion(declaracion_detalle_id=resp_dict['id'],
                                               rfc=resp_dict['rfc'],
                                               filed_timestamp=resp_dict['filed_timestamp'],
                                               filing_type=resp_dict['filing_type'],
                                               complimentary_type=resp_dict['complimentary_type'],
                                               filed_on=resp_dict['filed_on'],
                                               total_paid_due=resp_dict['total_paid_due'],
                                               is_paid=resp_dict['is_paid'],
                                               bank=resp_dict['bank'],
                                               paid_on=resp_dict['paid_on'],
                                               payment_operation=resp_dict['payment_operation'],
                                               filed_filing_file=resp_dict['filed_filing_file'],
                                               receipt_filing_file=resp_dict['receipt_filing_file'],
                                               paid_filing_file=resp_dict['paid_filing_file'],
                                               payment_filing_file=resp_dict['payment_filing_file'],
                                               filing_period=resp_dict['filing_period'],
                                               filing_period_type=resp_dict['filing_period']['period_type'],
                                               filing_period_year=resp_dict['filing_period']['year'],
                                               filing_period_period=resp_dict['filing_period']['period'],
                                               taxes=getTaxes(resp_dict['taxes']),
                                               users_detalle_declaracion_declaracion_id=user_id,
                                               json_filing_detail=resp_dict,
                                               )
    queryset.save()


def detalleDePeriodo(user_id, id_periodo, token_listo, request):

    url = 'https://listo.mx/api/filings/filing_periods/'+str(id_periodo)+''

    payload = {}
    headers = {
        'Authorization': 'Token '+token_listo+''
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp_dict = json.loads(response.text)
    if 'detail' in resp_dict:
        return 1
    else:
        filings = resp_dict['filings']
        diots = resp_dict['diots']
        x = 0
        for item in filings:
            queryset = Declaraciones(users_declaraciones_id=user_id,
                                     rfc=filings[x]['rfc'],
                                     filing_period=filings[x]['filing_period'],
                                     filing_id=filings[x]['id'],
                                     filed_timestamp=filings[x]['filed_timestamp'],
                                     operation_number=filings[x]['operation_number'],
                                     filing_type=filings[x]['filing_type'],
                                     filed_on=filings[x]['filed_on'],
                                     capture_line_expire_on=filings[x]['capture_line_expire_on'],
                                     days_to_pay=filings[x]['days_to_pay'],
                                     general_status=filings[x]['general_status'],
                                     payment_status=filings[x]['payment_status'],
                                     unknown_payment_status=filings[x]['unknown_payment_status'],
                                     expired_taxes=filings[x]['expired_taxes'],
                                     capture_line=filings[x]['capture_line'],
                                     total_due=filings[x]['total_due'],
                                     total_paid_due=filings[x]['total_paid_due'],
                                     creditable_due=filings[x]['creditable_due'],
                                     compensable_due=filings[x]['compensable_due'],
                                     checksum=filings[x]['checksum'],
                                     is_paid=filings[x]['is_paid'],
                                     bank=filings[x]['bank'],
                                     paid_on=filings[x]['paid_on'],
                                     payment_operation=filings[x]['payment_operation'],
                                     filed_filing_file=filings[x]['filed_filing_file'],
                                     receipt_filing_file=filings[x]['receipt_filing_file'],
                                     paid_filing_file=filings[x]['paid_filing_file'],
                                     payment_filing_file=filings[x]['payment_filing_file'],
                                     json_filing=filings[x]
                                     )
            detalleDeclaraciones(user_id, filings[x]['id'], token_listo)
            queryset.save()
            x = x+1

        y = 0
        for item in diots:
            queryset2 = Diots(users_diots_id=user_id,
                              diot_id=diots[y]['id'],
                              rfc=diots[y]['rfc'],
                              model_version=diots[y]['model_version'],
                              folder=diots[y]['folder'],
                              diot_type=diots[y]['type'],
                              filed_on=diots[y]['filed_on'],
                              accountant=diots[y]['accountant'],
                              receipt=diots[y]['receipt'],
                              filing_period=diots[y]['filing_period'],
                              json_diot=diots[y])
            queryset2.save()
            y = y+1
        return 0


class ListoViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """User view set.
    Handle signup, login and account verification
    """

    serializer_class = UserModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['retrieve', 'update', 'partial_update', ]:
            permissions = [IsAuthenticated, IsProfileOwner | isCompanyAdmin]
        elif self.action in ['aprovado', 'registrarUsuarioListo', 'verificaListo', 'descargaFacturas', 'facturasEmitidas', 'facturasRecibidas', 'direccionLegal', 'lista69b', 'declaracionesDiots', 'retrieveAllInvoices', 'retriveList69B', 'opinionCumplimiento', 'calculoIngresos', 'calculoIndicadores', 'retriveOpinionCumplimiento', 'retriveLegalAddress']:
            permissions = []
        elif self.action in ['list', ]:
            permissions = [IsAuthenticated, isCompanyAdmin]
        elif self.action in ['invitation', ]:
            permissions = [IsAuthenticated, isCompanyAdmin]
        else:
            permissions = [IsAuthenticated, ]
        return (permission() for permission in permissions)

    def list(self, request, *args, **kwargs):
        response = super(UserViewSet, self).list(request, *args, **kwargs)
        return response

    @action(detail=False, methods=['post'])
    def aprovado(self, request, *args, **kwargs):

        response = "Hola esta lista la clase"

        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def registrarUsuarioListo(self, request, *args, **kwargs):

        api = ListoApi(settings.LISTO_MASTER_TOKEN)

        if 'rfc' not in request.data or 'ciec' not in request.data:
            return Response('Falta rfc o ciec', status=status.HTTP_400_BAD_REQUEST)

        rfc_envio = request.data['rfc']
        ciec_envio = request.data['ciec']

        response = api.Setup.add_main_user(rfc=rfc_envio, ciec=ciec_envio)

        if 'customer_token' not in response:
            return Response('error ciec o rfc invalidos', status=status.HTTP_400_BAD_REQUEST)

        queryset2 = UserProfile.objects.get(user_id=request.data['id'])
        queryset2.rfc_id = response['customer_rfc_id']
        queryset2.token_listo = response['customer_token']
        queryset2.save()

        req = requests.get(
            'https://listo.mx/api/invoices/sat_sync_metadata/'+str(response['customer_rfc_id']),
            headers={'Authorization': 'Token '+response['customer_token']}
        )

        queryset3 = UserProfile.objects.get(user_id=request.data['id'])
        queryset3.num_regular_issued = req.json()['num_regular_issued']
        queryset3.num_crp_issued = req.json()['num_crp_issued']
        queryset3.num_payroll_issued = req.json()['num_payroll_issued']
        queryset3.num_crp_received = req.json()['num_crp_received']
        queryset3.num_regular_received = req.json()['num_regular_received']
        queryset3.num_payroll_received = req.json()['num_payroll_received']
        queryset3.save()

        return Response('Usuario registrado y completo', status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verificaListo(self, request, *args, **kwargs):

        api = ListoApi(settings.LISTO_MASTER_TOKEN)

        if 'rfc' not in request.data or 'ciec' not in request.data:
            return Response('Falta rfc o ciec', status=status.HTTP_400_BAD_REQUEST)

        rfc_envio = request.data['rfc']
        ciec_envio = request.data['ciec']

        try:
            response = api.Setup.add_main_user(rfc=rfc_envio, ciec=ciec_envio)
        except Exception as ex:
            return Response('error ciec o rfc invalidos', status=status.HTTP_400_BAD_REQUEST)

        return Response('RFC y Ciec validos', status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def descargaFacturas(self, request, *args, **kwargs):

        if 'token' not in request.data or 'id' not in request.data:
            return Response('Error en usuario', status=status.HTTP_400_BAD_REQUEST)

        token = request.data['token']

        url = "https://listo.mx/api/invoices/export_json?size=1000"

        payload = {}
        headers = {
            'Authorization': 'Token '+request.data['token']+''
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        resp_dict2 = json.loads(response.text)
        info_total = resp_dict2['results']

        size_array = resp_dict2['count']

        size = 1000
        offset = 1000
        offset = str(offset)
        lista_total_informacion = []

        while size_array > size:
            url = "https://listo.mx/api/invoices/export_json?size=1000&offset="+offset+""
            payload = {}
            headers = {
                'Authorization': 'Token '+request.data['token']+''
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            resp_dict2 = json.loads(response.text)
            info_total = resp_dict2['results'] + info_total
            size = size + 1000
            offset = int(offset)
            offset = offset + 1000
            offset = str(offset)

        x = 0
        for item in info_total:
            queryset = Facturas(
                issuer_rfc=info_total[x]['issuer_rfc'],
                issuer_name=info_total[x]['issuer_name'],
                is_income=info_total[x]['is_income'],
                receiver_rfc=info_total[x]['receiver_rfc'],
                payment_method=info_total[x]['payment_method'],
                receiver_name=info_total[x]['receiver_name'],
                validation_status_short=info_total[x]['validation_status_short'],
                validation_status=info_total[x]['validation_status'],
                modified_on=info_total[x]['modified_on'],
                total_pass_through_taxes_by_type_mxn=info_total[x]['total_pass_through_taxes_by_type_mxn'],
                subtotal=info_total[x]['subtotal'],
                exchange_rate=info_total[x]['exchange_rate'],
                cfdi_type=info_total[x]['cfdi_type'],
                iva=info_total[x]['iva'],
                iva_rate=info_total[x]['iva_rate'],
                discounts=info_total[x]['discounts'],
                adjusted_subtotal=info_total[x]['adjusted_subtotal'],
                uuid=info_total[x]['uuid'],
                factura_id=info_total[x]['id'],
                total_cents=info_total[x]['total_cents'],
                currency=info_total[x]['currency'],
                total_retained_taxes_by_type_mxn=info_total[x]['total_retained_taxes_by_type_mxn'],
                payment_form_display=info_total[x]['payment_form_display'],
                is_payroll=info_total[x]['is_payroll'],
                canceled_on=info_total[x]['canceled_on'],
                total=info_total[x]['total'],
                folio=info_total[x]['folio'],
                issued_on=getDate(info_total[x]['issued_on']),
                customer_id=info_total[x]['customer_id'],
                certified_on=info_total[x]['certified_on'],
                xml_file_ids=info_total[x]['xml_file_ids'],
                pdf_file_ids=info_total[x]['pdf_file_ids'],
                lineitems=info_total[x]['lineitems'],
                receiver_address=info_total[x]['receiver_address'],
                payroll_data=info_total[x]['payroll_data'],
                users_user_id=request.data['id'],
                json_invoice=info_total[x])
            detalleFactura(request.data['id'], info_total[x]['id'], request.data['token'])
            queryset.save()
            x = x+1

        return Response(resp_dict2['results'], status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def retrieveAllInvoices(self, request, *args, **kwargs):

        queryset2 = Facturas.objects.filter(issuer_rfc=request.data['rfc'], users_user_id=request.data['id'])
        data = serializers.serialize('json', queryset2)
        data = json.loads(data)

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def retriveList69B(self, request, *args, **kwargs):
        queryset2 = Lista69b.objects.filter(users_lista69b_id=request.data['id'])
        data = serializers.serialize('json', queryset2)
        data = json.loads(data)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def direccionLegal(self, request, *args, **kwargs):

        url = "https://listo.mx/api/filings/get_legal_address/"+request.data['rfc_id']+""

        payload = {}
        headers = {
            'Authorization': 'Token '+request.data['token']+''
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        resp_dict = json.loads(response.text)

        queryset = DireccionLegal(act_eco=resp_dict['Actividades economicas'],
                                  estatus_domicilio=resp_dict['Estatus Domicilio'],
                                  estatus_cont_dom=resp_dict['Estatus Contribuyente en domicilio'],
                                  fecha_alta_dom=resp_dict['Fecha Alta Domicilio'],
                                  ad=resp_dict['AD'],
                                  nomb_ent_fed=resp_dict['Nombre de la Entidad Federativa'],
                                  nomb_muni_demar_terri=resp_dict['Nombre del Municipio o Demarcacion Territorial'],
                                  nombre_localidad=resp_dict['Nombre de la Localidad'],
                                  nombre_colonia=resp_dict['Nombre de la Colonia'],
                                  nombre_vialidad=resp_dict['Nombre de vialidad'],
                                  numero_exterior=resp_dict['Numero exterior'],
                                  numero_interior=resp_dict['Numero interior'],
                                  entre_calle=resp_dict['Entre calle'],
                                  y_calle=resp_dict['Y calle'],
                                  tipo_vialidad=resp_dict['Tipo Vialidad'],
                                  cod_pos=resp_dict['Codigo Postal'],
                                  tipo_inmueble=resp_dict['Tipo de Inmueble'],
                                  tel_fijo=resp_dict['Tel. fijo'],
                                  tel_movil=resp_dict['Tel. movil'],
                                  correo=resp_dict['Correo'],
                                  referencia=resp_dict['Referencias'],
                                  json_direccion_legal=resp_dict,
                                  users_direccion_id=request.data['id']
                                  )
        queryset.save()

        return Response(resp_dict, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def lista69b(self, request, *args, **kwargs):

        url = 'https://listo.mx/api/counterparties/blacklist?size=1000'

        payload = {}
        headers = {
            'Authorization': 'Token '+request.data['token']+''
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        resp_dict = json.loads(response.text)
        resp_dict = resp_dict['result']

        x = 0
        for item in resp_dict:
            queryset = Lista69b(counterparty_rfc=resp_dict[x]['counterparty_rfc'],
                                rfc_name=resp_dict[x]['rfc_name'],
                                state=resp_dict[x]['state'],
                                list_type=resp_dict[x]['list_type'],
                                status=resp_dict[x]['status'],
                                entry_date=resp_dict[x]['entry_date'],
                                folio=resp_dict[x]['folio'],
                                customer_name=resp_dict[x]['customer_name'],
                                customer_rfc=resp_dict[x]['customer_rfc'],
                                users_lista69b_id=request.data['id'])
            queryset.save()
            x = x+1

        return Response(resp_dict, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def declaracionesDiots(self, request, *args, **kwargs):

        url = 'https://listo.mx/api/filings/rfcs/'+request.data['rfc_id']+'/status?size=1000'

        payload = {}
        headers = {
            'Authorization': 'Token '+request.data['token']+''
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        resp_dict = json.loads(response.text)
        resp_dict = resp_dict['filing_periods']
        count_filing_exists = 0
        x = 0
        for item in resp_dict:
            queryset = DeclaracionesDiots(users_declaracionesdiots_id=request.data['id'],
                                          filing_period_id=resp_dict[x]['id'],
                                          period_type=resp_dict[x]['period_type'],
                                          period=resp_dict[x]['period'],
                                          year=resp_dict[x]['year'],
                                          total_paid_due=resp_dict[x]['total_paid_due'],
                                          filing_due_on=resp_dict[x]['filing_due_on'],
                                          diot_due_on=resp_dict[x]['diot_due_on'],
                                          payment_status=resp_dict[x]['payment_status'],
                                          period_description=resp_dict[x]['period_description'],
                                          period_type_description=resp_dict[x]['period_type_description'],
                                          general_status=resp_dict[x]['general_status'],
                                          diot_general_status=resp_dict[x]['diot_general_status'],
                                          days_to_pay=resp_dict[x]['days_to_pay'],
                                          days_to_file=resp_dict[x]['days_to_file'],
                                          to_be_paid_due=resp_dict[x]['to_be_paid_due'],
                                          compensable_due=resp_dict[x]['compensable_due'],
                                          payable_due=resp_dict[x]['payable_due'],
                                          checksum=resp_dict[x]['checksum'],
                                          nearest_payment_on=resp_dict[x]['nearest_payment_on'],
                                          last_payment_on=resp_dict[x]['last_payment_on'],
                                          last_filing_filed_on=resp_dict[x]['last_filing_filed_on'],
                                          days_to_file_diot=resp_dict[x]['days_to_file_diot'],
                                          last_diot_filed_on=resp_dict[x]['last_diot_filed_on'],
                                          expired_taxes=resp_dict[x]['expired_taxes'],
                                          has_unkown_payment_status=resp_dict[x]['has_unkown_payment_status'],
                                          period_only_description=resp_dict[x]['period_only_description'],
                                          period_short_description=resp_dict[x]['period_short_description'],
                                          creditable_due=resp_dict[x]['creditable_due'],
                                          taxes=resp_dict[x]['taxes'],
                                          capture_line_expire_on=resp_dict[x]['capture_line_expire_on'],
                                          has_complementary_filings=resp_dict[x]['has_complementary_filings'],
                                          json_filings_diots=resp_dict)
            filing_not_declare = detalleDePeriodo(
                request.data['id'], resp_dict[x]['id'], request.data['token'], request)
            count_filing_exists = count_filing_exists + filing_not_declare
            queryset.save()
            x = x+1
        result = {
            'resp_dict': resp_dict,
            'count_filing_exists': count_filing_exists
        }
        return Response(result, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def opinionCumplimiento(self, request, *args, **kwargs):

        url = 'https://listo.mx/api/filings/fulfillment_opinion/'+request.data['rfc']+''

        payload = {}
        headers = {
            'Authorization': 'Token '+request.data['token']+''
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        resp_dict = json.loads(response.text)

        queryset = OpinionCumplimiento(
            fulfillment_opinion=resp_dict['Opinion de cumplimiento'],
            json_fulfillment_opinion=resp_dict,
            users_opinioncumplimiento_id=request.data['id']
        )
        queryset.save()

        return Response(resp_dict, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def retriveOpinionCumplimiento(self, request, *args, **kwargs):

        queryset = OpinionCumplimiento.objects.filter(users_opinioncumplimiento_id=request.data['id'])
        data = serializers.serialize('json', queryset)
        data = json.loads(data)

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def retriveLegalAddress(self, request, *args, **kwargs):

        queryset = DireccionLegal.objects.filter(users_direccion_id=request.data['id'])
        data = serializers.serialize('json', queryset)
        data = json.loads(data)

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def calculoIndicadores(self, request, *args, **kwargs):
        # Opinion de Cumplimiento
        opinion_cumplimiento = OpinionCumplimiento.objects.filter(users_opinioncumplimiento_id=request.data['id'])
        opinion_cumplimiento = serializers.serialize('json', opinion_cumplimiento)
        opinion_cumplimiento = json.loads(opinion_cumplimiento)
        # Calculo de INGRESOS
        ingresos = connection.cursor()
        ingresos.execute('''
           SELECT SUM(Total),SUM(Subtotal),rfc, MIN(periodo_minimo), MAX(periodo_maximo), SUM(cantidad)
            FROM (
            SELECT issuer_rfc AS rfc,
            MIN(issued_on) AS periodo_minimo,
            MAX(issued_on) AS periodo_maximo,
                    COUNT(issuer_rfc) Cantidad,
                    SUM(TO_NUMBER(subtotal_mxn, '99999999999D999S')) Subtotal,
                    SUM(TO_NUMBER(total_mxn, '99999999999D999S')) Total
            FROM listo_api_detalle_factura a
            WHERE issuer_rfc = %s AND
            is_income = true AND
                    canceled_on IS NULL AND
                    issued_on BETWEEN %s AND %s
            GROUP BY issuer_rfc
            UNION ALL
            SELECT payer_rfc AS rfc,
            MIN(issued_on) AS periodo_minimo,
            MAX(issued_on) AS periodo_maximo,
                    COUNT(issuer_rfc) Cantidad,
                    SUM(TO_NUMBER(subtotal_mxn, '99999999999D999S')) Subtotal,
                    SUM(TO_NUMBER(total_mxn, '99999999999D999S')) Total
            FROM listo_api_detalle_factura a
            WHERE payer_rfc = %s AND
            is_income = true AND
                    is_payroll = true AND
                    canceled_on IS NULL AND
                    issued_on BETWEEN  %s AND %s
            GROUP BY payer_rfc
            ORDER BY 1) as Ingresos
            GROUP BY rfc;
             ''', [request.data['rfc'], request.data['inicio'], request.data['fin'], request.data['rfc'], request.data['inicio'], request.data['fin']])
        user_ingresos = ingresos.fetchone()

        # Calculo de EGRESO
        egreso = connection.cursor()
        egreso.execute('''
        SELECT SUM(TO_NUMBER(total_mxn, '99999999999D99S')), SUM(TO_NUMBER(subtotal_mxn, '99999999999D99S')),
        MIN(issued_on),MAX(issued_on),COUNT(issuer_rfc)
        FROM public.listo_api_detalle_factura a
        WHERE payer_rfc = %s AND
        is_income = false AND
        is_payroll = false AND
        canceled_on IS NULL AND issued_on BETWEEN %s AND %s
        ORDER BY 1;
        ''', [request.data['rfc'], request.data['inicio'], request.data['fin']])
        user_egresos = egreso.fetchone()

        # Calculo de NOMINA PAGADA
        nomina_pagada = connection.cursor()
        nomina_pagada.execute(
            '''
             SELECT 
           SUM(TO_NUMBER(total, '99999999999D99S')) ,
           SUM(TO_NUMBER(subtotal, '99999999999D99S')) ,
           receiver_rfc,
           MIN(issued_on),
           MAX(issued_on),
            COUNT(receiver_rfc) 
           FROM listo_api_facturas a
           WHERE receiver_rfc = %s AND
           is_income = true AND
            is_payroll = true AND
            canceled_on IS NULL AND
            issued_on BETWEEN %s AND %s
            GROUP BY receiver_rfc
            ORDER BY 1;
            ''', [request.data['rfc'], request.data['inicio'], request.data['fin']])
        nomina_pagadas = nomina_pagada.fetchone()
        # Calculo de NOMINA PAGADA CANCELADA
        nomina_pagada_c = connection.cursor()
        nomina_pagada_c.execute(
            '''
             SELECT 
           SUM(TO_NUMBER(total, '99999999999D99S')) ,
           SUM(TO_NUMBER(subtotal, '99999999999D99S')) ,
           receiver_rfc,
           MIN(issued_on),
           MAX(issued_on),
            COUNT(receiver_rfc) 
           FROM listo_api_facturas a
           WHERE receiver_rfc = %s AND
           is_income = true AND
            is_payroll = true AND
            canceled_on IS NOT NULL AND
            issued_on BETWEEN %s AND %s
            GROUP BY receiver_rfc
            ORDER BY 1;
            ''', [request.data['rfc'], request.data['inicio'], request.data['fin']])
        nomina_pagada_c = nomina_pagada_c.fetchone()
        # Calculo de INGRESOS CANCELADOS
        ingresos_cancelados = connection.cursor()
        ingresos_cancelados.execute(
            '''
            SELECT SUM(Total), SUM(Subtotal), rfc, MIN(periodo_minimo), MAX(periodo_maximo), SUM(cantidad)
            FROM ( SELECT issuer_rfc as rfc, MIN(canceled_on) as periodo_minimo, MAX(canceled_on) as periodo_maximo,
                    COUNT(issuer_rfc) Cantidad,
                    SUM(TO_NUMBER(subtotal, '99999999999D99S')) Subtotal,
                    SUM(TO_NUMBER(total, '99999999999D99S')) Total
            FROM listo_api_facturas
            WHERE issuer_rfc = %s AND
                            is_income = true AND
                    canceled_on IS NOT NULL AND
                    canceled_on BETWEEN %s AND %s
            GROUP BY issuer_rfc
            UNION ALL
            SELECT payer_rfc AS rfc,
            MIN(canceled_on) as periodo_minimo,
            MAX(canceled_on) as periodo_maximo,
                    COUNT(payer_rfc) Cantidad,
                    SUM(TO_NUMBER(subtotal, '99999999999D99S')) Subtotal,
                    SUM(TO_NUMBER(total_mxn, '99999999999D99S')) Total
            FROM listo_api_detalle_factura a
            WHERE payer_rfc = %s AND
                            is_income = true AND
                    is_payroll = true AND
                    canceled_on IS NOT NULL AND
                    canceled_on BETWEEN %s AND %s
            GROUP BY payer_rfc
            ORDER BY 1) as Ingresos
            GROUP BY rfc;
            ''', [request.data['rfc'], request.data['inicio'], request.data['fin'], request.data['rfc'], request.data['inicio'], request.data['fin']]
        )

        ingresos_cancelados = ingresos_cancelados.fetchone()
        # Calculo de EGRESO CANCELADO
        egresos_cancelados = connection.cursor()
        egresos_cancelados.execute(
            '''
            SELECT SUM(TO_NUMBER(total, '99999999999D99S')), COUNT(issuer_rfc), payer_rfc, 
            MIN(canceled_on),
            MAX(canceled_on)
            FROM public.listo_api_detalle_factura
            WHERE payer_rfc = %s AND
            is_income = false AND
            is_payroll = false AND
            canceled_on IS NOT NULL AND
            canceled_on BETWEEN %s AND %s
            GROUP BY payer_rfc;
            ''', [request.data['rfc'], request.data['inicio'], request.data['fin']])
        egresos_cancelados = egresos_cancelados.fetchone()

        # Calculo de GRAFICAS
        graficas = connection.cursor()
        graficas.execute(
            '''
           SELECT DATE_PART('YEAR', issued_on)*100+
            DATE_PART('MONTH', issued_on) Mes,
                    CASE
                    WHEN is_income = true AND canceled_on IS NULL THEN 'INGRESO'
                    WHEN is_income = false AND is_payroll = True  THEN 'NOMINA'
                    WHEN is_income = false AND is_payroll = false AND canceled_on IS NULL AND TO_NUMBER(subtotal_mxn, '99999999999D99S') >= 0 THEN 'EGRESO'
                    WHEN is_income = false AND is_payroll = false AND TO_NUMBER(subtotal_mxn, '99999999999D99S') < 0 THEN 'NOTA_CREDITO'
						ELSE 'DESCONOCIDO'
                    END flujo,
                    COUNT(issuer_rfc) Cantidad,
                    ABS(SUM(TO_NUMBER(subtotal_mxn, '99999999999D99S'))) Subtotal,
                    ABS(SUM(TO_NUMBER(total_mxn, '99999999999D99S'))) Total
            FROM public.listo_api_detalle_factura a
            WHERE ((issuer_rfc =  %s  ) OR (payer_rfc = %s )) AND
                    issued_on BETWEEN %s AND %s
            GROUP BY DATE_PART('YEAR', issued_on),
            DATE_PART('MONTH', issued_on),
                     flujo
            ORDER BY 3, 1, 2;
            ''', [request.data['rfc'], request.data['rfc'], request.data['inicio'], request.data['fin']])

        # Calculo Graficas_C
        graficas_c = connection.cursor()
        graficas_c.execute(
            '''
            SELECT DATE_PART('YEAR', issued_on)*100+
            DATE_PART('MONTH', issued_on) Mes,
                    CASE
                    WHEN is_income = true THEN 'INGRESO_C'
                    WHEN is_income = true AND is_payroll = true  THEN 'NOMINA_C'
                    WHEN is_income = false AND is_payroll = false AND TO_NUMBER(subtotal_mxn, '99999999999D99S') >= 0 THEN 'EGRESO_C'
                    WHEN is_income = false AND is_payroll = false AND TO_NUMBER(subtotal_mxn, '99999999999D99S') < 0 THEN 'NOTA_CREDITO'
                    ELSE 'DESCONOCIDO'
                    END flujo,
                    COUNT(issuer_rfc) Cantidad,
                    ABS(SUM(TO_NUMBER(subtotal_mxn, '99999999999D99S'))) Subtotal,
                    ABS(SUM(TO_NUMBER(total_mxn, '99999999999D99S'))) Total
            FROM public.listo_api_detalle_factura a
            WHERE ((issuer_rfc =  %s ) OR (payer_rfc = %s )) AND
                    canceled_on IS NOT NULL AND
                    canceled_on BETWEEN %s AND %s
            GROUP BY DATE_PART('YEAR', issued_on),
            DATE_PART('MONTH', issued_on),
                     flujo
            ORDER BY 3, 1, 2;
            ''', [request.data['rfc'], request.data['rfc'], request.data['inicio'], request.data['fin']])

        # Calculo de DECLARACIONES
        declaraciones = connection.cursor()
        declaraciones.execute(
            '''
            SELECT listo_api_detalle_declaracion_declaracion.filing_period_period, listo_api_detalle_declaracion_declaracion.filing_period_type,
            CASE
            WHEN COUNT(listo_api_detalle_declaracion_declaracion.filing_period_period) = 0 THEN False
            ELSE True
            END Presentada
            FROM listo_api_declaraciones_periodos LEFT JOIN listo_api_detalle_declaracion_declaracion ON  
            listo_api_declaraciones_periodos.fecha_periodo = listo_api_detalle_declaracion_declaracion.filing_period_period
	        WHERE listo_api_detalle_declaracion_declaracion.rfc = %s AND listo_api_declaraciones_periodos.fecha_periodo BETWEEN %s AND %s  
            GROUP BY listo_api_detalle_declaracion_declaracion.filing_period_period,listo_api_detalle_declaracion_declaracion.filing_period_type
            ORDER BY 1;
            ''', [request.data['rfc'], request.data['inicio'], request.data['fin']])
        # Calculo de CFDI's EMITIDOS
        cfdis_e = connection.cursor()
        cfdis_e.execute('''
          SELECT COUNT(payer_rfc)
          FROM listo_api_detalle_factura
          WHERE (payer_rfc = %s OR issuer_rfc = %s ) AND issued_on BETWEEN %s AND %s  AND is_income = true;
            ''', [request.data['rfc'], request.data['rfc'], request.data['inicio'], request.data['fin']])
        cfdis_e = cfdis_e.fetchone()

        # Calculo de CFDI's RECIBIDOS
        cfdis_r = connection.cursor()
        cfdis_r.execute('''
          SELECT COUNT(payer_rfc)
          FROM listo_api_detalle_factura
          WHERE (payer_rfc = %s OR issuer_rfc = %s) AND issued_on BETWEEN %s AND %s AND is_income = false;
            ''', [request.data['rfc'], request.data['rfc'], request.data['inicio'], request.data['fin']])
        cfdis_r = cfdis_r.fetchone()

        # Semaforo declaraciones
        filing_semaforo = connection.cursor()
        filing_semaforo.execute('''
          	SELECT filing_period_year, COUNT(filing_period_year), CASE WHEN COUNT(filing_period_year) = 13 THEN TRUE
	        ELSE FALSE END ALL_FILINGS
	        FROM listo_api_detalle_declaracion_declaracion 
	        WHERE  rfc = %s AND filing_period_period BETWEEN %s AND %s
	        GROUP BY filing_period_year;
            ''', [request.data['rfc'], request.data['inicio'], request.data['fin']])

        data = {
            'egresos_c': egresos_cancelados,
            'ingresos_c': ingresos_cancelados,
            'nomina_pagada': nomina_pagadas,
            'nomina_pagada_c': nomina_pagada_c,
            'egresos': user_egresos,
            'ingresos': user_ingresos,
            'graficas': graficas,
            'graficas_c': graficas_c,
            'declaraciones': filing_semaforo,
            'opinion_cumplimiento': opinion_cumplimiento,
            'cfdis_e': cfdis_e,
            'cfdis_r': cfdis_r,
            'filing_semaforo': filing_semaforo
        }
        return Response(data, status=status.HTTP_200_OK)

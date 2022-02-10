from rest_framework import serializers

from taxinnovation.apps.listo_api.models import Facturas, DireccionLegal, Lista69b, DeclaracionesDiots, OpinionCumplimiento

class InformacionModelSerializer(serializers.ModelSerializer):
    """ User Profile Model Serializer. """

    class Meta:
        model = Facturas
        fields = (
            'issuer_rfc',
            'issuer_name',
            'receiver_rfc',
            'is_income',
            'payer_rfc',
            'payer_name',
            'is_payroll',
            'total',
            'canceled_on',
            'json_invoice'
        )

class OpinionCumplimientonModelSerializer(serializers.ModelSerializer):
    """ User Profile Model Serializer. """

    class Meta:
        model = OpinionCumplimiento
        fields = (
            'fulfillment_opinion',
            'fulfillment_opinion_pdf_text',
            'json_fulfillment_opinion',
        )

class DireccionLegalModelSerializer(serializers.ModelSerializer):
    """ User Profile Model Serializer. """

    class Meta:
        model = DireccionLegal
        fields = (
            'users_direccion',
            'act_eco',
            'estatus_domicilio',
            'estatus_cont_dom',
            'fecha_alta_dom',
            'ad',
            'nomb_ent_fed',
            'nomb_muni_demar_terri',
            'nombre_localidad',
            'nombre_colonia',
            'nombre_vialidad',
            'numero_exterior',
            'numero_interior',
            'entre_calle',
            'y_calle',
            'tipo_vialidad',
            'cod_pos',
            'tipo_inmueble',
            'tel_fijo',
            'tel_movil',
            'correo',
            'referencia'
        )

    
class Lista69bModelSerializer(serializers.ModelSerializer):
    """ User Profile Model Serializer. """

    class Meta:
        model = Lista69b
        fields = (
            'counterparty_rfc',
            'rfc_name',
            'state',
            'list_type',
            'status',
            'entry_date',
            'folio',
            'customer_name',
            'customer_rfc',
            'users_lista69b'
        )


class DeclaracionesDiotsModelSerializer(serializers.ModelSerializer):
    """ DeclaracionesDiots Model Serializer. """

    class Meta:
        model = DeclaracionesDiots
        fields = (
            'users_diots',
            'id_dec',
            'period_type',
            'period',
            'year',
            'total_paid_due',
            'filing_due_on',
            'diot_due_on',
            'payment_status',
            'period_description',
            'period_type_description',
            'general_status',
            'diot_general_status',
            'days_to_pay',
            'days_to_file',
            'to_be_paid_due',
            'compensable_due',
            'payable_due',
            'checksum',
            'nearest_payment_on',
            'last_payment_on',
            'last_filing_filed_on',
            'days_to_file_diot',
            'last_diot_filed_on',
            'expired_taxes',
            'has_unkown_payment_status',
            'period_only_description',
            'period_short_description',
            'creditable_due',
            'taxes',
            'capture_line_expire_on',
            'has_complementary_filings'
        )
from rest_framework import serializers

from taxinnovation.apps.catalogs.models import PostalCodeCatalog
from taxinnovation.apps.catalogs.serializers.addresses import PostalCodeCatalogSerializer
from taxinnovation.apps.users.models import ContactUser, UserAddress, ContactUserAddress


class ContactAddressModelSerializer(serializers.ModelSerializer):
    postal_code = PostalCodeCatalogSerializer(read_only=True)
    postal_code_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=PostalCodeCatalog.objects.all(), source='postal_code')

    class Meta:
        model = ContactUserAddress
        fields = [
            'id',
            'street',
            'external_num',
            'internal_num',
            'postal_code',
            'postal_code_id'
        ]


class ContactUserModelSerializer(serializers.ModelSerializer):
    """ User Profile Model Serializer. """
    address = ContactAddressModelSerializer(many=False, read_only=True, source='contactuseraddress')
    address_add = ContactAddressModelSerializer(many=False, write_only=True)

    class Meta:
        model = ContactUser
        fields = (
            'name',
            'last_name',
            'second_last_name',
            'email',
            'phone_number',
            'address',
            'address_add',
        )


class UserAddressModelSerializer(serializers.ModelSerializer):
    postal_code = PostalCodeCatalogSerializer(read_only=True)
    postal_code_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=PostalCodeCatalog.objects.all(), source='postal_code')

    class Meta:
        model = UserAddress
        fields = [
            'id',
            'street',
            'external_num',
            'internal_num',
            'postal_code',
            'postal_code_id'
        ]

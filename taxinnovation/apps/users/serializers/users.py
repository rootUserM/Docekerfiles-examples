from rest_framework import serializers
import os
import environ
from taxinnovation.apps.users.models import User, UserProfile, contact_user
from taxinnovation.apps.users.serializers.contact_user import ContactUserModelSerializer
from taxinnovation.apps.users.models import UserTemporalMedia
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from google.cloud import storage

class UserProfileModelSerializer(serializers.ModelSerializer):
    """ User Profile Model Serializer. """

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'picture',
            'role',
            'kind_of_person',
            'business_name',
            'rfc',
            'ciec',
            'constitutive_act',
            'official_identification_front',
            'official_identification_back',
            'proof_of_address',
            'authority_doc',
            'curp',
            'validation_video',
            'latitud',
            'longitud',
            'num_regular_issued',
            'num_crp_issued',
            'num_payroll_issued',
            'num_regular_received',
            'num_crp_received',
            'num_payroll_received',
            'ip_client',
            'rfc_id',
            'url_documento',
            'ticket_documento',
            'token_listo'
        )
        extra_kwargs = {
            'kind_of_person': {
                'required': True
            }
        }


class UserTemporalMediaModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTemporalMedia
        fields = (
            'id',
            'constitutive_act',
            'proof_of_address',
            'official_identification_front',
            'official_identification_back',
            'authority_doc',
            'validation_video',
            'curp'
        )


class UserModelSerializer(serializers.ModelSerializer):
    """ User Model serializer."""
    userprofile = UserProfileModelSerializer()
    contactuser = ContactUserModelSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'last_name',
            'second_last_name',
            'email',
            'is_taxadmin',
            'phone_number',
            'userprofile',
            'contactuser',
            'contract_sended',
            'contract_signed',
            'aprovado'
        )
        read_only_fields = ('username', )

    def create(self, validated_date):
        return super(UserModelSerializer, self).create(validated_date)


class TemporalMigrationToUserSerializer(serializers.Serializer):
    temp_id = serializers.IntegerField(
        required=True
    )
    user_id = serializers.IntegerField(
        required=True
    )

    def validate(self, attrs):
        media_id = attrs['temp_id']
        user_id = attrs['user_id']
        media_queryset = UserTemporalMedia.objects.filter(id=media_id)
        user_queryset = User.objects.filter(id=user_id)
        if not user_queryset.exists():
            raise serializers.ValidationError('Id de usuario no existe')
        elif not media_queryset.exists():
            raise serializers.ValidationError('Id de tabla media no existe')
        return attrs

    def create(self, validated_data):
        media_id = validated_data['temp_id']
        user_id = validated_data['user_id']

        user = UserProfile.objects.get(user_id=user_id)

        temp_files = UserTemporalMedia.objects.get(id=media_id)
        # Migracion de media, de temporalMedia a tabla usuario
        user.constitutive_act = temp_files.constitutive_act
        user.official_identification_front = temp_files.official_identification_front
        user.official_identification_back = temp_files.official_identification_back
        user.proof_of_address = temp_files.proof_of_address
        user.authority_doc = temp_files.authority_doc
        user.validation_video = temp_files.validation_video
        user.curp = temp_files.curp
        user.save()

        return validated_data


class HelpTicketSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True)

    def validate(self, data):
        """if the email has an associated account send the recovery email."""
        email = data['email']
        user = User.objects.filter(email=email)

        if user.exists():
            self.send_email_ticket(user[0], data)

        return data

    def send_email_ticket(self, user: User, data):
        """Send the ticket Email."""
        subject = 'Nuevo Ticket De Ayuda'
        from_email = 'Contacto <{}>'.format(settings.EMAIL_HOST_USER)
        html_message = render_to_string(
            'emails/help_ticket.html',
            {
                'message': data['message'],
                'user': user
            }
        )
        recipient_list = [user.email, ]

        send_mail(subject=subject, from_email=from_email, message=None,
                  recipient_list=recipient_list, fail_silently=False, html_message=html_message)

class UpdatePhotoSerializer(serializers.Serializer):
    picture = serializers.ImageField(required=True)
    email = serializers.EmailField(required=True)


    def validate(self, data):
        """if the email has an associated account send the recovery email."""
        email = data['email']
        user = User.objects.filter(email=email)
        if user.exists():
           self.change_picture(user[0], data)

        return users_picture

    def change_picture(self, user: User, data):
        profile = UserProfile.objects.get(user_id=user.id)
        profile.picture = data['picture']
        # profile.save()
        return profile
        

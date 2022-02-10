from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from datetime import timedelta

import jwt
from rest_framework_simplejwt import settings as jwt_settings
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# noinspection PyAbstractClass
from taxinnovation.apps.users.models import (
    User,
    UserProfile, ContactUser, UserAddress, ContactUserAddress
)


# noinspection PyAbstractClass
from taxinnovation.apps.users.serializers.contact_user import ContactUserModelSerializer, UserAddressModelSerializer
from taxinnovation.apps.users.serializers.users import UserProfileModelSerializer
from django.contrib.auth.hashers import make_password


class UserLoginTokenPairSerializer(TokenObtainSerializer):
    """"""

    def get_token(self, user, request):
        token = RefreshToken.for_user(user)

        # User avatar
        try:
            picture_url = user.userprofile.picture.url
        except ValueError:
            picture_url = '#'

        picture_url = request.build_absolute_uri(picture_url) if picture_url != '#' else '#'

        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['is_taxadmin'] = user.is_taxadmin

        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }

        request = self.context['request']

        user = authenticate(**authenticate_kwargs)

        if user is None:
            # raise exceptions.AuthenticationFailed('Revise sus credenciales')
            return {'status': 'Revise sus credenciales', 'pass': False}

        if not user.is_active or not user.is_verified:
            return {'status': 'La cuenta no ha sido verificada aún, revise su email.', 'pass': False}
            # raise exceptions.AuthenticationFailed('La cuenta no ha sido verificada aún, revise su email.')

        if not user.contract_sended:
            return {'status': 'La cuenta está siendo verificada por nuestros ejecutivos.', 'pass': False}
            # raise exceptions.AuthenticationFailed('La cuenta está siendo verificada por nuestors ejecutivos.')

        if not user.contract_signed:
            return {'status': 'El contrato aun no ha sido firmado.', 'pass': False}
            # raise exceptions.AuthenticationFailed('El contrato aun no ha sido firmado.')

        if not user.aprovado:
            return {'status': 'La cuenta aún no ha sido aprobada', 'pass': False}
            # raise exceptions.AuthenticationFailed('El contrato aun no ha sido firmado.')

        if user.is_active and user.is_verified and user.contract_sended and user.contract_signed and user.aprovado:
            refresh = self.get_token(user, request)
            return {'refresh': str(refresh), 'access': str(refresh.access_token), 'pass': True}


class PasswordRecoveryEmail(serializers.Serializer):
    email = serializers.EmailField(required=True)

    @staticmethod
    def gen_verification_token(user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'jti': jwt_settings.api_settings.JTI_CLAIM,
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'token_type': 'password_recovery'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

    def validate(self, data):
        """if the email has an associated account send the recovery email."""
        email = data['email']
        user = User.objects.filter(email=email)

        if user.exists():
            self.send_email_recovery(user[0])

        return data

    def send_email_recovery(self, user: User):
        """Send the email password recovery."""
        current_site = Site.objects.get(id=1)
        full_path_domain = '{}{}'.format(current_site, '/auth/password_reset')
        verification_token = self.gen_verification_token(user)
        subject = 'Tu contraseña de  TAX INNOVATION'
        from_email = 'Contacto <{}>'.format(settings.EMAIL_HOST_USER)
        html_message = render_to_string(
            'emails/account_recovery.html',
            {
                'full_path_domain': full_path_domain,
                'verification_token': verification_token,
                'user': user
            }
        )
        recipient_list = [user.email, ]

        send_mail(subject=subject, from_email=from_email, message=None,
                  recipient_list=recipient_list, fail_silently=False, html_message=html_message)


class PasswordRecovery(serializers.Serializer):
    password = serializers.CharField(
        min_length=8,
        max_length=64,
        required=True
    )
    password_confirmation = serializers.CharField(
        min_length=8,
        max_length=64,
        required=True
    )
    token = serializers.CharField(required=True)

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Link de verificación ha expirado')
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError('Token inválido')

        if payload['token_type'] != 'password_recovery':
            raise serializers.ValidationError('Token inválido')

        self.context['payload'] = payload

        return data

    def validate(self, data):
        """Verifies passwords match."""
        password = data['password']
        password_confirmation = data['password_confirmation']
        token = data['token']

        if password != password_confirmation:
            raise serializers.ValidationError('Las contraseñas no coinciden')

        # Password valid or raise exception
        password_validation.validate_password(password)
        self.validate_token(token)

        # Validate if exists the user
        try:
            User.objects.get(username=self.context['payload']['user'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuario no encontrado')

        return data

    def save(self):
        user = User.objects.get(username=self.context['payload']['user'])
        user.set_password(self.validated_data['password'])
        user.save()

        # Send the token to blacklist
        # token = SlidingToken(self.validated_data['token'], verify=False)
        # token.blacklist()

        return user


class UserSignUpSerializer(serializers.ModelSerializer):
    """User signup serializer.
    Handle sign up data validation and user/profile creation.
    """
    userprofile = UserProfileModelSerializer(many=False, read_only=True)
    userprofile_add = UserProfileModelSerializer(many=False, write_only=True)
    contactuser = ContactUserModelSerializer(many=False, read_only=True)
    contactuser_add = ContactUserModelSerializer(many=False, write_only=True)
    address = UserAddressModelSerializer(many=False, read_only=True, source='useraddress')
    address_add = UserAddressModelSerializer(many=False, write_only=True)

    password = serializers.CharField(
        min_length=8,
        max_length=64,
        required=True,
        write_only=True
    )
    password_confirmation = serializers.CharField(
        min_length=8,
        max_length=64,
        required=True,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'last_name',
            'second_last_name',
            'email',
            'phone_number',
            'userprofile',
            'userprofile_add',
            'password',
            'password_confirmation',
            'contactuser',
            'contactuser_add',
            'address',
            'address_add',
        )

    def validate(self, data):
        """Verifies passwords match."""
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError('Las contraseñas no coinciden')

        # Password valid or raise exception
        password_validation.validate_password(password)

        return data

    def create(self, validated_data):
        """Handle user and profile creation"""
        validated_data.pop('password_confirmation')
        userprofile_add = validated_data.pop('userprofile_add')
        address_add = validated_data.pop('address_add')
        contactuser_add = validated_data.pop('contactuser_add')

        # Removiendo el Contact User - addressAdd
        contactuser_address_add = contactuser_add.pop('address_add')

        user = User.objects.create_user(**validated_data)

        # Almacena el perfil del usuario
        UserProfile.objects.create(
            user=user,
            **userprofile_add,
        )

        # Almacena el usuario de contacto
        contact_user = ContactUser.objects.create(
            user=user,
            **contactuser_add,
        )

        # Almacena la dirección del usuario
        UserAddress.objects.create(**address_add, user_id=user.id)

        # Almacena la dirección del usuario contacto
        ContactUserAddress.objects.create(**contactuser_address_add, user_id=contact_user.id)

        current_site = Site.objects.get(id=1)
        login_url = '{}{}'.format(current_site, '/auth/ConfirmacionCorreoView')

        self.send_verify_account_email(user=user, full_path_domain=login_url)
        return user

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.name,
            'email': user.email,
            'username': user.username,
            'exp': int(exp_date.timestamp()),
            'token_type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def send_verify_account_email(self, user: User, full_path_domain: str):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = '¡Bienvenido @{}! Verifica tu cuenta para comenzar a usar TAX INNOVA'.format(user.name)
        from_email = 'Contacto <{}>'.format(settings.EMAIL_HOST_USER)
        html_message = render_to_string(
            'emails/account_verification.html',
            {
                'full_path_domain': full_path_domain,
                'verification_token': verification_token,
                'user': user
            }
        )
        recipient_list = [user.email, ]

        send_mail(subject=subject, from_email=from_email, message=None,
                  recipient_list=recipient_list, fail_silently=False, html_message=html_message)


class UserInvitationSerializer(serializers.Serializer):
    """User invitation serializer."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    username = serializers.CharField(
        min_length=4,
        max_length=32,
        required=True
    )
    name = serializers.CharField(
        min_length=2,
        max_length=120,
        required=True
    )
    last_name = serializers.CharField(
        min_length=2,
        max_length=45,
        required=True
    )
    second_last_name = serializers.CharField(
        min_length=2,
        max_length=45,
        required=False,
        allow_blank=True
    )
    phone_number = serializers.CharField(
        min_length=10,
        max_length=10,
        required=True
    )

    def save(self):
        current_site = Site.objects.get(id=1)
        signup_url = '{}{}'.format(current_site, '/auth/signup')

        """Handle user creation to send the email"""
        email = self.validated_data['email']
        name = self.validated_data['name']
        last_name = self.validated_data['last_name']
        second_last_name = self.validated_data['second_last_name']
        phone_number = self.validated_data['phone_number']

        self.send_invitation_email(
            email=email,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
            phone_number=phone_number,
            full_path_domain=signup_url,
        )

    @staticmethod
    def gen_verification_token(
        email: str,
        name: str,
        last_name: str,
        second_last_name: str,
        phone_number: str,
    ):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'email': email,
            'name': name,
            'lastName': last_name,
            'secondLastName': second_last_name,
            'phoneNumber': phone_number,
            'exp': int(exp_date.timestamp()),
            'token_type': 'emaiConfirmation',
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

    def send_invitation_email(
            self,
            email: str,
            name: str,
            last_name: str,
            second_last_name: str,
            phone_number: str,
            full_path_domain: str,
    ):
        """Send email invitation link to new user."""
        verification_token = self.gen_verification_token(
            email=email,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
            phone_number=phone_number,
        )
        subject = 'Has recibido una invitación para usar TAX INNOVATION'
        from_email = 'Contacto <{}>'.format(settings.EMAIL_HOST_USER)
        html_message = render_to_string(
            'emails/account_invitation.html',
            {
                'verification_token': verification_token,
                'full_path_domain': full_path_domain,
            }
        )
        recipient_list = [email, ]

        send_mail(subject=subject, from_email=from_email, message=None,
                  recipient_list=recipient_list, fail_silently=False, html_message=html_message)


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Link de verificación ha expirado')
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError('Token inválido')

        if payload['token_type'] != 'email_confirmation':
            raise serializers.ValidationError('Token inválido')

        self.context['payload'] = payload

        return data

    def save(self, **kwargs):
        """Update the user's verified active and status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['username'])
        user.is_verified = True
        user.is_active = True
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    username = serializers.CharField(
        min_length=4,
        max_length=32,
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verifies user data."""

        # Verifies passwords match
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError('Las contraseñas no coinciden')

        password_validation.validate_password(password)

        try:
            user = User.objects.get(username=data['username'])
            user.password = make_password(password, salt=None, hasher='default')
            user.save()
        except User.DoesNotExist:
            raise serializers.ValidationError('No existe ninguna cuenta asociada')

        data['username'] = "Ok"

        return data


class SendEmailChangePasswordSerializer(serializers.Serializer):
    model = User

    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        try:
            user = User.objects.get(email=email)
            self.send_email_resetpass(user)
        except User.DoesNotExist:
            raise serializers.ValidationError('No existe ninguna cuenta asociada')

        data['EMAIL'] = "Ok"

        return data

    def send_email_resetpass(self, user):
        """Send account reset pass."""
        current_site = Site.objects.get(id=1)
        full_path_domain = '{}{}'.format(current_site, '/auth/password_reset')
        verification_token = self.gen_verification_token(user)
        subject = 'Actualización de contraseña'
        from_email = 'Contacto <{}>'.format(settings.EMAIL_HOST_USER)
        html_message = render_to_string(
            'emails/account_recovery.html',
            {
                'full_path_domain': full_path_domain,
                'verification_token': verification_token,
                'user': user
            }
        )
        recipient_list = [user.email, ]

        send_mail(subject=subject, from_email=from_email, message=None,
                  recipient_list=recipient_list, fail_silently=False, html_message=html_message)

    @staticmethod
    def gen_verification_token(user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'name': user.name,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

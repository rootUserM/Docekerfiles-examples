"""Users views."""

from rest_framework import viewsets, mixins, status
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taxinnovation.apps.users.models import User, UserAddress, contact_user
from taxinnovation.apps.users.permissions.users import isCompanyAdmin, IsAccountOwner, IsProfileOwner
from taxinnovation.apps.users.serializers.users import ( UserModelSerializer, UserProfileModelSerializer,
 UserTemporalMediaModelSerializer, TemporalMigrationToUserSerializer, HelpTicketSerializer ,UpdatePhotoSerializer )
from taxinnovation.apps.users.serializers.contact_user import UserAddressModelSerializer
from taxinnovation.apps.users.models import UserTemporalMedia, UserProfile, User

from .firmamex import FirmamexServices
import json

from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(mixins.CreateModelMixin,
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
        elif self.action in ['profile', 'get_document_info', 'web_hook_firmamex', 'aprovado', 'helpTicket']:
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

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            'user': response.data
        }
        response.data = data
        return response

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update Profile data."""
        user = self.get_object()
        userprofile = user.userprofile
        partial = request.method == 'PATCH'

        serializer = UserProfileModelSerializer(
            instance=userprofile,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user, context={'request': request}).data
        return Response(data)

    def get_queryset(self):
        """Overrides the queryset if is necessary."""
        queryset = User.objects.prefetch_related('userprofile').filter()
        if self.action in ['list', ]:
            """Get only active users."""
            return queryset.filter(is_verified=True)
        if self.action in ['signup']:
            return queryset
        return queryset.filter(is_verified=True)

    @action(detail=False, methods=['post'])
    def get_document_info(self, request, *args, **kwargs):

        webid = "P1LrZjTYkxZHnp3g"
        apikey = "7a792eb717f0a58366ea2c502bcc8d4f"
        services = FirmamexServices(webid, apikey)

        response = services.getReport(request.data['ticket'])

        json_respuesta = json.loads(response)

        return Response(json_respuesta['allSigned'], status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def web_hook_firmamex(self, request, *args, **kwargs):
        webid = "P1LrZjTYkxZHnp3g"
        apikey = "7a792eb717f0a58366ea2c502bcc8d4f"
        services = FirmamexServices(webid, apikey)

        response = services.getReport(request.data['firmamex_id'])

        json_respuesta = json.loads(response)

        if json_respuesta['allSigned'] == True:
            queryset = UserProfile.objects.get(ticket_documento=request.data['firmamex_id'])
            id_usuario = queryset.user_id
            queryset.save()
            queryset2 = User.objects.get(id=id_usuario)
            queryset2.contract_signed = True
            queryset2.save()
            respuesta = True
        else:
            respuesta = False

        return Response(json_respuesta['allSigned'], status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def aprovado(self, request, *args, **kwargs):

        queryset2 = User.objects.get(id=request.data['id'])
        queryset2.aprovado = True
        queryset2.save()
        response = True

        # SELECT COUNT(issuer_rfc) FROM cfdis_factura WHERE issuer_rfc=(user rfc);

        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def helpTicket(self, request, *args, **kwargs):
        serializer = HelpTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'])
    def changePPhoto(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data['email'])
        profile = UserProfile.objects.get(user_id=user[0].id)
        profile.picture = request.data['picture']
        user_picture = profile.picture
        profile.save()
        response = {
            'picture': user_picture.url
        }
        print(response)
        return Response(response,status=status.HTTP_201_CREATED)


class UserTemporalMediaViewSet(viewsets.ModelViewSet):
    queryset = UserTemporalMedia.objects.all()
    serializer_class = UserTemporalMediaModelSerializer

    @action(detail=False, methods=['post'], url_path='attach-temp-media-to-user-profile')
    def attach_temp_media_to_user_profile(self, request, *args, **kwargs):
        """Transefer media to user."""

        serializer = TemporalMigrationToUserSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


class UserAdressRetrieveViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']


class UserAprovadoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['aprovado']

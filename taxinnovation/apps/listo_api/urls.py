"""Users URLs."""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView


from rest_framework.routers import DefaultRouter

from taxinnovation.apps.users.views.auth import UserAuthViewSet
from taxinnovation.apps.users.views.users import UserViewSet, UserTemporalMediaViewSet, UserRetrieveViewSet, UserAdressRetrieveViewSet, UserAprovadoViewSet
from taxinnovation.apps.users.views.pubsub import UserPubSubViewSet
from taxinnovation.apps.listo_api.views.listo import ListoViewSet

router = DefaultRouter()
router.register(r'listo_api', ListoViewSet, basename='listo_api')

app_name = 'listo_api'

urlpatterns = [
    path('', include((router.urls, 'listo_api'), namespace='listo_api'))
]
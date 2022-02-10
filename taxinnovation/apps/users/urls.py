"""Users URLs."""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView


from rest_framework.routers import DefaultRouter

from taxinnovation.apps.users.views.auth import UserAuthViewSet
from taxinnovation.apps.users.views.users import UserViewSet, UserTemporalMediaViewSet, UserRetrieveViewSet, UserAdressRetrieveViewSet, UserAprovadoViewSet
from taxinnovation.apps.users.views.pubsub import UserPubSubViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', UserAuthViewSet, basename='auth')
router.register(r'pubsub', UserPubSubViewSet, basename='pubsub')
router.register(r'user-temp-media', UserTemporalMediaViewSet, basename='user_temp_media')
router.register(r'user-retrive-info', UserRetrieveViewSet, basename='user-retrive-info')
router.register(r'user-retrive-adress', UserAdressRetrieveViewSet, basename='user-retrive-adress')
router.register(r'user-retrive-aprovado', UserAprovadoViewSet, basename='user-retrive-aprovado')

app_name = 'users'

urlpatterns = [
    path('', include((router.urls, 'auth'), namespace='auth')),
    path('token/', include([  # noqa DJ05
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
    ])),
]

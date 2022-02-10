"""Users tests."""

from rest_framework.test import APITestCase

from django.urls import reverse

from taxinnovation.apps.users.models import User


class UsersAPITestCase(APITestCase):
    """ Get users lists"""

    def setUp(self):
        """Test case setup"""
        self.company_admin = User.objects.create(
            name='Nombre',
            last_name='Las Name',
            email='admin@admin.com',
            username='admin',
            is_active=True,
            is_verified=True
        )

    def test_get_token(self):
        """Verify the token auth"""
        url = reverse('users:auth:auth-token')
        request = self.client.get(url)

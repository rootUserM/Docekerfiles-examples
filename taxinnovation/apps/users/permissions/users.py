"""Users permissions classes."""

from rest_framework.permissions import BasePermission

from taxinnovation.apps.users.models import UserProfile


class isCompanyAdmin(BasePermission):
    """Allow access only to company admins."""

    def has_permission(self, request, view):
        """Verify user has a membership ."""
        try:
            UserProfile.objects.get(
                user=request.user,
                is_active=True,
            )
            return True

        except UserProfile.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """Verify user has a membership"""

        try:
            UserProfile.objects.get(
                user=request.user,
                is_active=True,
            )
            return True

        except UserProfile.DoesNotExist:
            return False


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same."""
        return request.user == obj.user


class IsProfileOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same."""
        return request.user == obj


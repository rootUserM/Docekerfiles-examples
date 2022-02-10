"""User models admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Models
from taxinnovation.apps.users.models import User, ContactUser, UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'name', 'is_active', 'is_verified',
                    'last_name', 'is_staff', 'created_at')
    list_filter = ('is_superuser', 'is_staff', 'created_at', 'modified_at')
    list_editable = ('is_active', 'is_verified',)
    inlines = (
        ProfileInline,
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'last_name', 'second_last_name', 'phone_number', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'user__email', 'user__name', 'user__last_name')


@admin.register(ContactUser)
class ContactUserModelAdmin(admin.ModelAdmin):
    """Profile model admin."""
    list_display = ('id', 'user', 'name', 'last_name', 'email')
    list_display_links = ('id', 'user')
    search_fields = ('user__email', 'user__name', 'user__last_name')


admin.site.register(User, CustomUserAdmin)

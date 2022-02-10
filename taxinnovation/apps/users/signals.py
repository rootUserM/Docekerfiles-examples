from taxinnovation.apps.users.models.users import User
from taxinnovation.apps.users.models.profiles import UserProfile

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_post_save(sender, update_fields, created, instance, **kwargs):
    if instance.is_superuser and created:
        UserProfile.objects.create(
            user_id=instance.id,
        )
        instance.is_active = True
        instance.is_verified = True
        instance.save()

from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = 'taxinnovation.apps.users'
    verbose_name = 'Usuarios'

    def ready(self):
        import taxinnovation.apps.users.signals  # noqa

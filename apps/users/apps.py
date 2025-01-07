from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    label = 'users'
    
    def ready(self):
        try:
            import apps.users.signals  # noqa
        except ImportError:
            pass

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
    verbose_name = "Gestion des notifications"

    def ready(self):
        import notifications.signals  # noqa: F401

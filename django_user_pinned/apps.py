from django.apps import AppConfig


class SingleSessionConfig(AppConfig):
    """
    The app config for the single_session app.
    """

    name = "django_user_pinned"
    verbose_name = "django user pinned"
    default_auto_field = "django.db.models.BigAutoField"

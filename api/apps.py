from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .signals import log_user_logged_in_failed, log_user_logged_in_success

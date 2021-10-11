from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "api"
    verbose_name = "MPASocial API"

    def ready(self):
        import api.signals

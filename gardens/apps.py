from django.apps import AppConfig


class GardensConfig(AppConfig):
    name = 'gardens'

    def ready(self):
        # Django Signals
        import gardens.signals


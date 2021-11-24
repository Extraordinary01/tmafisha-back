from django.apps import AppConfig


class AfishaConfig(AppConfig):
    name = 'afisha'

    def ready(self):
        import afisha.signals

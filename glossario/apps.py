from django.apps import AppConfig

class GlossarioConfig(AppConfig):
    name = 'glossario'
    def ready(self):
        import glossario.signals

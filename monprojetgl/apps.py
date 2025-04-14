from django.apps import AppConfig


class MonprojetConfig(AppConfig):
    name = 'monprojetgl'  # Doit correspondre exactement au nom du package
    label = 'monprojetgl'  # Enlevez le '_unique' pour la cohérence
    verbose_name = "Mon Projet GL"
    
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        import monprojetgl.signals



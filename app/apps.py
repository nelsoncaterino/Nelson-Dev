from django.apps import AppConfig as DjangoAppConfig
from django.db import models

class AppConfigCustom(DjangoAppConfig):  # ✅ classe renommée proprement
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

def ready(self):
    print("App is ready!")  # Debug
    import app.signals
from django.apps import AppConfig

# imports for scheduler
from django.apps import AppConfig
import threading
import time
from django.core.management import call_command



class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    #def ready(self):
        # Function to repeatedly process background tasks


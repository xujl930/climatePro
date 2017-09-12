from django.apps import AppConfig

from .signals import create_auth_token

class ClimateappConfig(AppConfig):
    name = 'climateApp'

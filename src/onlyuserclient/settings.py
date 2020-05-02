""" onlyuser client配置
"""
from django.conf import settings
from rest_framework.settings import APISettings

user_settings = getattr(settings,'ONLYUSERCLIENT',None)

default_settings = {
    'API_ROOT_URL': '',
    'API_TIMEOUT': 30,
    'API_HEADERS': {},
    'APIKEY_HEADER': 'apikey',
    'APIKEY': None,
    'CACHE_API': False,
    'CACHE_TTL': 60,
} 

api_settings = APISettings(user_settings,default_settings,None)
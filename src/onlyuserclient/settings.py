""" onlyuser client配置
"""
from django.conf import settings
from rest_framework.settings import APISettings

user_settings = getattr(settings,'ONLYUSERCLIENT',None)

default_settings = {
    'API_ROOT_URL': '',
    'ONLYUSER_PFX': None,
    'BILLING_PFX': None,
    'API_TIMEOUT': 30,
    'API_HEADERS': {},
    'APIKEY_HEADER': 'apikey',
    'APIKEY': None,
    'CACHE_API': False,
    'CACHE_TTL': 60,
    'HAS_ROLE': True,
    # 本地模式,如果允许，将不会访问远程服务器
    'LOCAL': False,        
} 

api_settings = APISettings(user_settings, default_settings, None)
onlyuser_settings = api_settings

billing_user_settings = getattr(settings, 'BILLINGCLIENT', None)

billing_default_settings = {
    # 计费服务器RPC主机名
    'RPC_HOST': 'localhost',
    # 计费服务器RPC端口     
    'RPC_PORT': 18812,
    # RPC超时(秒)
    'RPC_TIMEOUT': 5,
    # 计费服务器Restful接口URL
    'API_ROOT_URL': None,
    # 计费服务器Restful接口超时(秒)
    'API_TIMEOUT': 30,
    # 计费服务器Restful接口附加Http Header
    'API_HEADERS': {},
    # 计费服务器Restful接口使用apikey鉴权，包括KEY的Header
    'APIKEY_HEADER': 'apikey',
    # apikey鉴权KEY
    'APIKEY': None,
    # 缓存远程接口
    'CACHE_API': False,
    # 缓存存活时间(秒)
    'CACHE_TTL': 60,
    # 检查应用对组织计费
    'ORGANIZATION_BILL': True,
    # 检查应用对用户计费
    'USER_BILL': False,
    # 此项目提供的服务项目列表
    'SERVICES': {},
    # 本地模式,如果允许，将不会访问远程服务器
    'LOCAL': False,    
}
billing_settings = APISettings(billing_user_settings, billing_default_settings, None)

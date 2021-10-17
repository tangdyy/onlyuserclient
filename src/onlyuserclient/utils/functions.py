'''处理器工具函数
'''
import importlib
from onlyuserclient.settings import billing_settings
from onlyuserclient.settings import onlyuser_settings
from onlyuserclient.handler import BillApiHandler
from django.core.cache import caches, cache


def get_billapi_handler(
    service_key,
    before=True,
    after=True,
    usable=True,
    application_service=False
    ):
    '''返回一个API接口计费处理器对象.
    '''
    service_item = billing_settings.SERVICE_ITEMS.get(service_key, None)
    if service_item is None:
        raise ValueError('The service key is not a valid value.')
     
    if len(service_item) < 2:
        raise ValueError('settings BILLING.SERVICE_ITEMS key: %s error.'%(service_key,))

    service_label = service_item[0]
    bill_handler_module =  service_item[1]
    bill_handler_cls = None
    if bill_handler_module:
        arr = bill_handler_module.split('.')
        module_name = '.'.join(arr[:-1])
        cls_name = arr[-1:][0]
        module = importlib.import_module(module_name)
        bill_handler_cls = getattr(module, cls_name, None)
        if bill_handler_cls is None:
            raise ValueError('The service itme handler is not valid value.')
    else:
        bill_handler_cls = BillApiHandler
    
    handler = bill_handler_cls(
        service_label,
        before=before,
        after=after,
        usable=usable,
        application_service=application_service       
    ) 
    return handler


def get_bill_cache():
    if billing_settings.CACHE_ENGINE in caches:
        return caches[billing_settings.CACHE_ENGINE]
    return cache
    
def get_onlyuser_cache():
    if onlyuser_settings.CACHE_ENGINE in caches:
        return caches[onlyuser_settings.CACHE_ENGINE]
    return cache

def generate_cache_key(pfx, *args, **kwargs):
    keystr = ''
    for arg in args:
        keystr += '{}'.format(arg)
    for k, v in kwargs.items():
        keystr += '{}:{}'.format(k, v)
    return '{}:{}'.format(pfx, hash(keystr))
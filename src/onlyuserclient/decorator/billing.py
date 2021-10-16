import importlib
from functools import wraps
from django.http import HttpRequest
from django.utils import timezone
from onlyuserclient.settings import billing_settings

class api_charge():
    '''API计费装饰器类
    '''
    def __init__(self, 
        service_key, 
        before=True,
        after=True,
        usable=True,
        application_service=False
        ):
        if service_key is None or not service_key in billing_settings.SERVICE_ITEMS:
            raise ValueError('The service is not a valid value.')
        if len(billing_settings.SERVICE_ITEMS) < 2:
            raise ValueError('settings BILLING.SERVICE_ITEMS key: %s error.'%(service_key,))

        service_label = billing_settings.SERVICE_ITEMS[0]
        bill_handler_module =  billing_settings.SERVICE_ITEMS[1]
        bill_handler = None
        if bill_handler:
            bill_handler = importlib.reload(bill_handler_module)
        else:
            bill_handler = importlib.reload('onlyuserclient.handler.BillApiHandler')

        class BillConfig():
            pass
        self.config = BillConfig()
        
        self.config.service_label = service_label
        self.config.bill_handler = bill_handler
        self.config.before = before
        self.config.after = after
        self.config.usable = usable
        self.config.application_service = application_service
 
    def __call__(self, func):
        setattr(func, '_bill_config', self.config)
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            
            response = func(*args, **kwargs)
            return response
        return wrapped_function

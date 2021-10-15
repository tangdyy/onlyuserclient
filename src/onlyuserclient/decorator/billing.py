from functools import wraps
from django.http import HttpRequest
from django.utils import timezone
from onlyuserclient.settings import billing_settings

class api_charge():
    '''API计费装饰器类
    '''
    def __init__(self, 
        service=None, 
        before=True,
        after=True,
        usable=True,
        organization_bill=None, 
        user_bill=None
        ):
        if service is None or not service in billing_settings.SERVICES:
            raise ValueError('The service is not a valid value.')
        self.config = {}
        self.config['service'] = service
        self.config['before'] = before
        self.config['after'] = after
        self.config['usable'] = usable
        self.config['organization_bill'] = organization_bill
        self.config['user_bill'] = user_bill

    def __call__(self, func):
        setattr(func, '__bill_config', self.config)
        print(dir(func), func.__name__, func.__module__, func.__qualname__)
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            response = func(*args, **kwargs)
            return response
        return wrapped_function

from functools import wraps
from django.http import HttpRequest
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

        self.service = service
        self.before = before
        self.after = after
        self.usable = usable
        self.organization_bill = organization_bill
        self.user_bill = user_bill
        
    def get_count(self):
        return 1

    def get_start_time(self):
        return None

    def get_finish_time(self):
        return None
 
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(request, *args, **kwargs):
            if request is None or  not isinstance(request, HttpRequest):
                raise ValueError(
                    "The first parameter of the function decorated with 'api_charge' must be 'HttpRequest' object."
                )
            print('decorator', request, args, kwargs)
            response = func(request, *args, **kwargs)
            setattr(request, 'bill', ('a', 'b'))
            return response
        return wrapped_function
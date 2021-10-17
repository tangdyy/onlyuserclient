from functools import wraps
from onlyuserclient.utils.functions import get_billapi_handler

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
        self.bill_handler = get_billapi_handler(
            service_key, 
            before,
            after,
            usable,
            application_service            
        )
 
    def __call__(self, func):
        setattr(func, '_bill_handler', self.bill_handler)
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            func._bill_handler.before_api(*args, **kwargs)
            response = func(*args, **kwargs)
            func._bill_handler.after_api(*args, **kwargs)
            return response
        return wrapped_function

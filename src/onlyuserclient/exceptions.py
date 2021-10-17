from rest_framework.exceptions import *
from rest_framework.views import exception_handler


API_ERROR_HTTP_CODE = 441

def onlyuserclient_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and  response.status_code == API_ERROR_HTTP_CODE:
        response.reason_phrase = 'Onlyuser Client Exception'

    return response


class OnlyuserclientApiException(APIException):
    '''API异常基类
    '''
    status_code = API_ERROR_HTTP_CODE
    default_detail = 'Onlyuser client API访问异常.'
    default_code = 'onlyuserclient_exception'
    default_error_code = 0    
    def __init__(self, code=None, detail=None, **kwargs):
        super().__init__()
        self.error_code = code or self.default_error_code
        self.status_code = kwargs.pop('status_code', None) or self.status_code
        self.detail = {
            'code': code or self.default_error_code,
            'detail': detail or self.default_detail
        }
        self.detail.update(kwargs)



class RestfulClientError(OnlyuserclientApiException):
    default_detail = 'API接口访问异常。'
    default_code = 'reatful_client_error'
    default_error_code = 700 
    def __init__(self, exec=None):
        status_code = None
        code = None
        detail = None
        response = getattr(exec, 'response', None)
        if response:
            status_code = response.status_code
            code = response.body.get('code', -1)
            detail = response.body.get('detail', None)
            if detail is None:
                detail = response.body.get('non_field_errors', None)   
                 
        super().__init__(code=code, detail=detail, status_code=status_code)


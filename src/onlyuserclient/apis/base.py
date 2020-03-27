from simple_rest_client import exceptions
from simple_rest_client.api import API
from simple_rest_client.models import Response
from simple_rest_client.resource import Resource

DEFAULT_API_TIMEOUT = 30 

class BaseAPI():
    """
    Base api
    """
    def __init__(self, api_root_url, timeout=DEFAULT_API_TIMEOUT):        
        self._api= API(api_root_url = api_root_url,
                       json_encode_body = True,
                       headers = {'Content-Type': 'application/json'},
                       append_slash = True,
                       timeout = timeout )        
        fun = getattr(self, 'register_resource')
        if fun is None:
            raise AttributeError("'register_resource' method must be defined.")
        fun()
        self._status = None
        self._error = {}

    @property
    def status(self):
        return self._status

    @property
    def error(self):
        return self._error                 


    def _request(self, resource, action, *args, body=None, params={}, headers={}, **kwargs):
        """ 
        请求restful
        @resource 资源名称
        @action   操作名
        @args     restful接口url中位置参数，如：/users/{id}/，id是一个位置参数
        @body     消息体数据
        @params   URL参数
        @headers  消息头部   
        """
        self._status = None
        self._error = None
        res = getattr(self._api,resource,None)
        if res is None:
            self._api.add_resource(resource_name=resource)
            res = getattr(self._api,resource) 
        act = getattr(res,action)
        response = None
        data = None

        try:
            response = act(*args, body=body, headers=headers, params=params, **kwargs)
        except Exception as e :
            if isinstance(e, exceptions.ClientConnectionError):
                self._error = {'client_connections_error':str(e)}
            elif isinstance(e, exceptions.ActionNotFound):       
                self._error = {'ation_not_found_error':str(e)}
            elif isinstance(e, exceptions.ActionURLMatchError):
                self._error = {'ation_url_match_error':str(e)}
            elif isinstance(e, exceptions.ErrorWithResponse):     
                response = getattr(e, 'response', None)
                err = getattr(response, 'body', None)
                if isinstance(err, dict):
                    self._error = err
                else:
                    self._error = {'errors': err}
            else:
                self._error = {'errors':str(e)} 

        if not response is None:
            self._status = response.status_code 
            data = response.body   
        return data       

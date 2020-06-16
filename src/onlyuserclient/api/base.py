from simple_rest_client.api import API
from onlyuserclient.settings import api_settings

DEFAULT_API_TIMEOUT = 30 

class BaseAPI(API):
    """
    Base api
    """
    def __init__(self, **kwargs):   
        url = kwargs.pop('api_root_url',api_settings.API_ROOT_URL)
        headers = kwargs.pop('headers',api_settings.API_HEADERS)
        headers.update({'Content-Type': 'application/json'})
        timeout = kwargs.pop('timeout',api_settings.API_TIMEOUT) or DEFAULT_API_TIMEOUT
        json_encode_body = kwargs.pop('json_encode_body ', True)
        append_slash = kwargs.pop('append_slash ', True)
        if api_settings.APIKEY:
            headers[api_settings.APIKEY_HEADER] = api_settings.APIKEY
            
        super().__init__(
            api_root_url=url,
            headers = headers,
            timeout = timeout,
            json_encode_body = json_encode_body,
            append_slash=append_slash,
            **kwargs
        )

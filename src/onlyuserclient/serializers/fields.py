from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import CharField, ChoiceField, Field, RelatedField, ValidationError
from onlyuserclient.utils import functions
from onlyuserclient.api import get_onlyuserapi
from onlyuserclient.settings import api_settings
from .serializers import ApiRelatedListSerializer


__all__ = (
    "HideCharField", 
    "RemotePkRelatedField", 
    "UserRelatedField", 
    "OrganizationRelatedField", 
    "SummaryRelatedField", 
    "SelecterField",
    "ApplicationRelatedField",
    "ApiRelatedField",
           
)

class HideCharField(CharField):
    '''可以部分隐藏的字符串字段
       初如化参数除了标准字符串字段的参数外,有以下专用参数:
       @fill_char     填充隐藏位置的字符
       @hide_start    隐藏开始位置,从0开始
       @hdie_end      隐藏结束位置,如果是-1则表示到结尾
    '''
    def __init__(self, *args, **kwargs):
        self._fill_char = kwargs.get('fill_char', '*')
        self._hide_start = kwargs.get('hide_start', 0)
        self._hide_end = kwargs.get('hide_end', -1)
        kw = kwargs
        if 'fill_char' in kw:
             kw.pop('fill_char') 
        if 'hide_start' in kw:
            kw.pop('hide_start') 
        if 'hide_end' in kw:
            kw.pop('hide_end') 
        super().__init__(*args, **kwargs) 

    def to_representation(self, value):
        data = super().to_representation(value)

        if self._hide_end<0:
            hide_str = data[self._hide_start:]
        else:
            hide_str = data[self._hide_start:self._hide_end]
        
        hide_len = len(hide_str)
        return data[:self._hide_start] + self._fill_char*hide_len + data[self._hide_start+hide_len:]
        
class RemotePkRelatedField(Field):
    '''远程主键关联字段,字段值是外部资源的ID
       
    '''
    def __init__(self, *args, resource=None, action='retrieve', fields=[], **kwargs):
        self._resource = resource
        self._action = action
        self._fields = fields  
        super().__init__(*args, **kwargs)

    def get_remote_object(self, value):
        cache_key = functions.generate_cache_key('RPRF', self._resource, value)
        obj = None
        if api_settings.CACHE_API:
            obj = cache.get(cache_key)
        if obj:
            return obj
        onlyuserapi = get_onlyuserapi()
        api = getattr(self, 'remote_api', onlyuserapi)
        res = getattr(api, self._resource, None)
        if res is None:
            raise Exception("Api not found resource '%s'."%(self._resource,))
        act = getattr(res, self._action, None)
        if act is None:
            raise Exception("Resource '%s' not found action '%s'."%(self._resource, self._action))

        try:
            response = act(value)
        except:
            raise Exception('Failed to access API interface.')

        if response is None or response.status_code != 200:
            raise Exception("ID:%s is not a valid object for resource '%s'."%(value, self._resource))  

        if api_settings.CACHE_API and  response.body:
            cache.set(cache_key, response.body, api_settings.CACHE_TTL)
        return response.body                

    def to_representation(self, value):
        try:
            obj = self.get_remote_object(value)
        except Exception:
            obj = None
        
        new_val = {'id':value}
        if obj:
            for field in self._fields:
                new_val[field] = obj.get(field, None)
        return new_val

    def to_internal_value(self, data):
        try:
            obj = self.get_remote_object(data)
        except Exception as e:
            obj = None
        if obj is None:
            raise ValidationError("ID:%s is not a valid object for resource '%s'."%(data, self._resource)) 
        return data

class UserRelatedField(RemotePkRelatedField):
    '''用户对象关联字段
    '''
    def __init__(self, *args, fields=['username', 'nickname'], **kwargs):
        super().__init__(*args, resource='users', action='retrieve', fields=fields, **kwargs)

class OrganizationRelatedField(RemotePkRelatedField):
    '''组织机构对象关联字段
    '''
    def __init__(self, *args, fields=['name'], **kwargs):
        super().__init__(*args, resource='organizations', action='retrieve', fields=fields, **kwargs)

class ApplicationRelatedField(RemotePkRelatedField):
    '''应用程序对象关联字段
    '''
    def __init__(self, *args, fields=['name'], **kwargs):
        super().__init__(*args, resource='applications', action='retrieve', fields=fields, **kwargs)
       
class SummaryRelatedField(RelatedField):
    """
    显示摘要信息, 可读写, 通过ID字段关联到目标, 参数fields指示返回的字段
    """

    def __init__(self, fields=None, **kwargs):
        self.fields = fields or []
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(id=data)
        except ObjectDoesNotExist:
            raise ValidationError('关联对象不存在')
        except (TypeError, ValueError):
            raise ValidationError('无效字段值')

    def to_representation(self, obj):
        result = {'id':obj.id}
        for field in self.fields:
            result[field] = getattr(obj, field)
        return result

class SelecterField(ChoiceField):
    '''选项对象字段
    '''
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if value in ('', None):
            return value
        obj = {
            'value': value,
            'label': self.choices.get(value, value)
        } 
        return obj




class ApiRelatedField(Field):
    '''Remot API associated field

    When serializing a list object, it should be paired with 'ApiRelatedListSequencer' to 
    reduce the number of API accesses.

    Args:
        api_url (str): API URL.
        param (str): associated id param name.
        fields (list): fields to return.
        objects (str): associated objects in API response path.
        pos (str): param position, query, body, path.
        auth (str): auth type, base, apikey, token, none.
        username (str): username for basic auth.
        password (str): password for basic auth.
        apikey (str): apikey for apikey auth.
        token (str): token for token auth.
        headers (dict): request headers.

    Example:
    ```
    class ApiRelatedDemoSerializer(serializers.ModelSerializer):
        owner = ApiRelatedField(
            api_url='http://127.0.0.1:8000/api/v2/users/', 
            param='id__in',
            fields=['id', 'username', 'nickname'],
            objects='results',
        )
        class Meta:
            model = User
            fields = "__all__"
            read_only_fields = []
            list_serializer_class = ApiRelatedListSerializer

    ```        
    '''
    def __init__(self, *args, **kwargs):
        self._api_url = kwargs.pop('api_url', None)
        self._method = kwargs.pop('method', 'GET').upper()
        self._fields = kwargs.pop('fields', None)
        self._objects = kwargs.pop('objects', None) 
        self._headers = kwargs.pop('headers', {})
        self._pos = kwargs.pop('pos', 'query')  # query, body, path
        self._param = kwargs.pop('param', 'id')
        self._auth = kwargs.pop('auth', None)  # base, apikey, token, none
        self._username = kwargs.pop('username', None)
        self._password = kwargs.pop('password', None)
        self._apikey = kwargs.pop('apikey', None)
        self._token = kwargs.pop('token', None)
        super().__init__(*args, **kwargs)

    def _get_headers(self):
        headers = self._headers.copy()
        if self._auth == 'base':
            return headers
        elif self._auth == 'apikey':
            headers['X-API-KEY'] = self._apikey
        elif self._auth == 'token':
            headers['Authorization'] = 'Bearer %s'%(self._token,)
        return headers

    def _request_api(self, value):
        if not self._api_url:
            raise Exception("ApiRelatedField need 'api_url' parameter.")       

        url = self._api_url
        if self._pos == 'path':
            if isinstance(value, list):  # path
                p = ','.join([str(val) for val in value])
            else:
                p = str(value)

            url = urljoin(self._api_url, p)
            params = {}
            data = {}
        elif self._pos == 'body':
            params = {}
            data = {self._param: value}
        else:  # query
            params = {self._param: value}
            data = {}
        
        if self._auth == 'base':
            auth = HTTPBasicAuth(self._username, self._password)
        else:
            auth = None

        if self._method == 'GET':
            response = requests.get(url, params=params, headers=self._get_headers(), auth=auth)
        elif self._method == 'POST':
            response = requests.post(url, params=params, data=data, headers=self._get_headers(), auth=auth)
        else:
            raise Exception("ApiRelatedField only support 'GET' and 'POST' method.")
        return response.json()

    def _get_related_objects(self, value):
        datas = self._request_api(value)
        if self._objects:
            for key in self._objects.split('.'):
                datas = datas[key]
        
        if self._fields:
            results = []
            for data in datas:
                obj = {}
                for field in self._fields:
                    obj[field] = data.get(field, None)
                results.append(obj)
            return results                    
        return datas

    def to_representation(self, value):
        if hasattr(self.root, 'many') and isinstance(self.root, ApiRelatedListSerializer):
            # In a list serializer, skip processing to avoid multiple calls
            return value
        
        objects = self._get_related_objects(value)
        if objects:
            return objects[0]
        return value
        
    def to_internal_value(self, data):
        return data

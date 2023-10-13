from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import CharField, ChoiceField, Field, RelatedField, ValidationError
from onlyuserclient.utils import functions
from onlyuserclient.api import get_onlyuserapi
from onlyuserclient.settings import api_settings

__all__ = (
    "HideCharField", 
    "RemotePkRelatedField", 
    "UserRelatedField", 
    "OrganizationRelatedField", 
    "SummaryRelatedField", 
    "SelecterField",
    "ApplicationRelatedField",
           
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
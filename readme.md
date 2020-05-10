# onlyuserclient

统一认证服务客户端,配合onlyuser在微服务中实现对象权限控制，包括数据记录和字段权限控制。    

## 依赖包
+ django >= 2.0.0
+ djangorestframework >= 3.10.0

## 安装
```shell
python setup.py install
```

## 快速开始

### 1.修改配置文件`settings.py`   
添加以下配置项：
+ 添加中间件`onlyuserclient.middlewares.RoleMiddleware`到配置中
  ```python
  
  MIDDLEWARE = [
      '....',
      'onlyuserclient.middlewares.RoleMiddleware',
  ]  

  ```
+ 添加`onlyuserclient`配置    
  ```python   
  ONLYUSERCLIENT ={
      'API_ROOT_URL': 'http://onlyuser-service.test.svc.cluster.local',
      'API_TIMEOUT': 30,
      'API_HEADERS': {},
      'APIKEY_HEADER': 'apikey',
      'APIKEY': '',    
      'CACHE_API': False,
      'CACHE_TTL': 60,    
  }
  ```   
  * API_ROOT_URL     
    onlyuser服务的根URL, 根据实际部署环境正确配置。   
  * API_TIMEOUT    
    onlyuser的API接口访问超时(秒), 默认30秒。    
  * API_HEADERS   
    需要附加到访问onlyuser的请求中的http header,  是一个健值对，KEY就header名，VALUE是header值。
  * APIKEY_HEADER   
    如果从集群外访问onlyuser，访问接口要求用`key-auth`方式鉴权，此配置项指定携带`KEY`的http header名称，默认是`apikey`，实际名称要与onlyuser服务端配置一致。    
  * APIKEY   
    `key-auth`的KEY，由onlyuser服务端提供。如果为`None`，表示不需要认证，默认是`None`。    
  * CACHE_API   
    是否在本地缓存API访问结果，默认是`False`。onlyuserclient是使用Django内建的缓存功能，当你开启此项时，还需要同时配置`settings.py`中的`CACHES`。    
  * CACHE_TTL    
    缓存有效时间，默认`60`秒。
  

### 2.确定字段权限控制方案，定义序列化类
确定要控制字段显示和字段修改权限的场景，并分别定义多个序列化类，每个场景对应一个序列化类，并定义一个标签。     
例如:  序列化类有三个字段`name`，`mobile`，`address`。第一种情况允许用户修改所有字段并完整显示全部字段, 用标签`all`代表；第二种情况用户不能修改`mobile`字段，并且隐藏`mobile`字段中间4位，用`*`号代替, 用标签`part`代表；第三种情况全部字段都只能查看不能修改，并且隐藏`address`字段, 用`*`号代替, 用标签`readonly`代表；定义三个序列化类
```python
from rest_framework import serializers
from .models import Demo
from onlyuserclient.serializers import HideCharField

class AllDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demo
        fields = "__all__"

class PartDemoSerializer(serializers.ModelSerializer):
    mobile = HideCharField(max_length=11, hide_start=3,hide_end=7, fill_char='*')
    class Meta:
        model = Demo
        fields = "__all__"
        read_only_fields = ['mobile']


class ReadonlyDemoSerializer(serializers.ModelSerializer):
    address = HideCharField(max_length=11, hide_start=0,hide_end=-1, fill_char='*')
    class Meta:
        model = Demo
        fields = "__all__"
        read_only_fields = ['name','mobile','address']
```

### 3.定义视图集类   
从`onlyuserclient.viewsets.RoleModelViewSet`继承。这个类默认实现了按组织机构控制的数据记录权限控制,定义了五个标签:    
+ `all`     
  可以访问全部记录   
+ `owner`   
  可以访问用户自已拥有的记录
+ `department`    
  可以访问本部门的全部用户的记录
+ `branch`    
  可以访问本部门及下属机构全部用户的记录
+ `organization`    
  可以操作所在组织整个组织机构树下全部用户的记录

视图类除了`ModelViewSet`的标准属性外，需要定义以下属性：  
+ `queryset` 
  必须定义，是Model的QuerySet对象。
+ `user_relate_field` 
  必须定义，Model中关联`User`的字段名，此字段保存`User`对象的`ID`值，类型为`CHAR(24)`。
+ `serializer_classs`  
  必须定义，`dict`类型，key是tag, value是序列化类。
+ `org_relate_field`
  可选，保存`Organization`对象`ID`，默认是关联到根组织。
+ `allow_not_auth`
  可选，是否允许未鉴权访问，默认`False`。  

```python
from onlyuserclient.viewsets import RoleModelViewSet
from .serializers import DefaultDemoSerializer, CompleteDemoSerializer, HideDemoSerializer
from .models import RoleDemo

class RoleViewSet(RoleModelViewSet):
    queryset = RoleDemo.objects.all()
    user_relate_field = 'owner'
    serializer_classs = {
        'default': DefaultDemoSerializer,
        'complete': CompleteDemoSerializer,
        'part': HideDemoSerializer
    }
```

### 4.相关序列化字段参考   
+ `HideCharField`    
  可以部分隐藏的字符串字段，除了标准属性外，有以下属性：
  + `fill_char`   
    隐藏部分的填充字符，默认是`*`。
  + `hide_start`   
    隐藏开始位置，从`0`开始。
  + `hide_end`   
    隐藏结束位置，如果`-1`，表示到结尾。
+ `RemotePkRelatedField`  
  主键远程关联字段，本地保存的字段值是远程资源的主键，有以下属性：
  + `resource`   
    远程资源名
  + `action`    
    查询资源对象的方法，默认就`retrieve`。
  + `fields`    
    序列化的资源字段列表
  + `remote_api`    
    一个`simple_rest_client.api.API`对象，访问远程资源，只能在子类中定义，默认是`onlyuserapi`。
+ `UserRelatedField`    
  onlyuser的`User`关联字段
+ `OrganizationRelatedField`    
  onlyuser的`Organization`关联字段

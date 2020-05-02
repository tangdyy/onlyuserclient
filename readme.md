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

首先修改配置文件`settings.py`
添加以下配置项：
+ 添加中间件`onlyuserclient.middlewares.RoleMiddleware`到配置中
  ```python
  
  MIDDLEWARE = [
      '....'
      'onlyuserclient.middlewares.RoleMiddleware',
  ]  

  ```
+ 添加配置项
  * onlyuser微服务的根URL
  ```python
  ONLYUSER_API_URL = 'http://127.0.0.1:8000' 
  ```
  * API接口访问超时(秒), 默认30秒
  ```python
  API_TIMEOUT = 5
  ```
  * onlyuser接口key-auth的KEY值,如是None表示不需要认证,默认是None
  ```python
  ONLYUSER_APIKEY='lLl8Mo1EE0Ydx7TyNkqRHllRosqdpDd0'
  ```
  * onlyuser接口携带key-auth KEY的http header名称
  ```python
  ONLYUSER_APIKEY_HEADER = 'apikey'
  ```
  

第二步确定要控制字段显示和字段修改权限的场景,并分别定义多个序列化类,每个场景对应一个序列化类,并定义一个标签。例如:    
序列化类有三个字段`name`,`mobile`,`address`。第一种情况允许用户修改所有字段并完整显示全部字段, 用标签`all`代表；第二种情况用户不能修改`mobile`字段,并且隐藏`mobile`字段中间4位,用`*`号代替, 用标签`part`代表；第三种情况全部字段都只能查看不能修改,并且隐藏`address`字段, 用`*`号代替, 用标签`readonly`代表；定义三个序列化类
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

第三步定义视图集类, 从`onlyuserclient.viewsets.RoleModelViewSet`继承。这个类默认实现了按组织机构控制的数据记录权限控制,定义了五个标签:    
+ `all` 可以访问全部记录
+ `owner` 可以访问用户自已拥有的记录
+ `department` 可以访问本部门的全部用户的记录
+ `branch` 可以访问本部门及下属机构全部用户的记录
+ `organization` 可以操作所在组织整个组织机构树下全部用户的记录

视图类除了`ModelViewSet`的标准属性外，需要定义以下属性：  
+ `queryset` 必须定义，是QuerySet对象
+ `user_relate_field` 必须定义，`Model`中关联`User`的字段名
+ ``
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
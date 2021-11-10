# onlyuserclient

统一认证服务Onlyuser客户端开发包,配合Onlyuser在微服务中实现：    
+ 角色权限控制，包括数据记录和字段权限控制。
+ 计费相关功能

## 依赖包
+ django >= 2.0.0
+ djangorestframework >= 3.10.0

## 安装
+ 源码包安装    
```shell
python setup.py install
```
+ pip安装  
```shell
pip install onlyuserclient  
# 升级
pip install -U onlyuserclient
```


## 快速开始

### 1.修改配置文件`settings.py`   

#### 1.1.添加中间件到配置中
  ```python
  
  MIDDLEWARE = [
      '....',
      # 角色权限中间件
      'onlyuserclient.middleware.RoleMiddleware',
      # 计费控制中间件
      'onlyuserclient.middleware.BillingMiddleware',
  ]  

  ```
#### 1.2.添加`onlyuserclient`配置    
  ```python   
  ONLYUSERCLIENT ={
      'API_ROOT_URL': 'http://dev.onlyuser',
      'API_TIMEOUT': 5,
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
#### 1.3.添加计费配配置项 <span id='1.3'></span>
  ```python
  BILLINGCLIENT = {
      # 计费服务器Restful接口URL
      'API_ROOT_URL': 'http://dev.billing',
      # API URL前缀
      'API_PFX': None,
      # 计费服务器Restful接口超时(秒)
      'API_TIMEOUT': 5,
      # 缓存远程接口
      'CACHE_API': False,
      # 缓存存活时间(秒)
      'CACHE_TTL': 60,
      # 属于应用服务
      'APPLICATION_SERVICE': True,
      # 此项目提供的服务项目列表
      'SERVICE_ITEMS': {
          'insurance': ('b6b962b2-198d-490d-bab1-14765212bbbe', '汽车保险算价服务  ', None),
      },
      # 缓存引擎
      'CACHE_ENGINE': 'cache',
      # 本地模式,如果允许，将不会访问远程服务器
      'LOCAL': False
  }
  ```  
  * API_ROOT_URL   
  计费服务器API接口的根URL
  * API_PFX      
  URL前缀
  * API_TIMEOUT        
  计费服务器Restful接口超时(秒)
  * CACHE_API     
  是否缓存远程接口访问数据，默认是`False`。      
  缓存接口访问数据可以大幅减少接口重复访问，极大提高后端性能，生产环境应当开启。   
  * CACHE_TTL     
  接口缓存数据的生命期，默认60秒。     
  此值大小需要权衡性能和数据更新及时性。   
  * APPLICATION_SERVICE     
  此项目是否属于应用服务, 默认`False`。    
  ***属于应用服务*** 是指此项目提供的功能是应用程序的基础服务，计费上将受应用程序类服务项目的控制，比如： ***名单管理*** 是 ***车险营销管理系统*** 的基础功能，不单独计费，***名单管理*** 微服务项目的配置项 `APPLICATION_SERVICE` 应当设为`True`。           
  在视图类中可以设置类属性 `application_service` 配置视图类是否属于应用服务。           
  在视图类方法的计费装饰器 `apiview_charge` 的初始化参数中可以设置参数 `application_service`，配置视图类方法是否属于应用服务。      
  这三个配置项的优先级：     
  配置项 `APPLICATION_SERVICE` > 类属性 `application_service` >  装饰器 `apiview_charge`参数 `application_service`
  * SERVICE_ITEMS      
  此项目提供的服务项目的计费配置，`dict`类型。格式如下： 
  ```python        
  {
      'key': ('计费服务项目的label', '服务项目名称', '计费处理类'),
      'insurance': ('b6b962b2-198d-490d-bab1-14765212bbbe', '汽车保险算价服务  ', None),
  }
  ```
  * CACHE_ENGINE     
  缓存引擎，django配置项`CACHES`的key值。生产环境建议用数据库、membercache等高性能缓存引擎。      
  * LOCAL    
  本地模式，如果允许，将不会访问远程服务器，用于代码编程阶段，不便于链接计费服务器时，默认是`False`。

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
+ `creater`   
  **v1.0.10 增加**。     
  可选，记录创建者字段名，如果有这个属性，将根据登录用户自动填充创建者和创建时间字段。    
  属性值：    
  * `True`, 默认字段名`creater`、`create_time`。   
  * `list`对象，自定义字段名，第一个元素是创建者字段名，第二个是创建时间字段名。    
+ `reviser`   
  **v1.0.10 增加**。     
  可选，记录修改者字段名，如果有这个属性，将根据登录用户自动填充修改者和修改时间字段。    
  属性值：    
  * `True`, 默认字段名`reviser`、`modify_time`。   
  * `list`对象，自定义字段名，第一个元素是修改者字段名，第二个是修改时间字段名。       
  

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
+ `SummaryRelatedField`      
  关联字段摘要信息字段
+ `ApplicationRelatedField`   
  onlyuser的`Application`关联字段
+ `SelecterField`   
  选项字段，在序列化类中定义属性`serializer_choice_field`，值等于`SelecterField`。        
  ``` 

### 5.`ChoicesModelMixin`类    
为模型视图类混入选项字段的选项列表查询方法。  
```python
class ResourceViewSet(RoleModelViewSet, ChoicesModelMixin):
    pass
```
查询选项列表URL    
```shell 
GET resources/choices
```
返回结果格式
```json
{
  "field1":[
    ["value1", "label1"],
    ["value2", "label2"]
  ],
  "field2":[
    ["value1", "label1"],
    ["value2", "label2"]
  ]
}
```

### 6.实现API接口计费方法    
+ 参照上面[1.3.](#1.3) 配置，并在 `SERVICE_ITEMS` 中添加计费服务项目配置。
+ 修改需要计费的视图类方法，添加装饰器 `apiview_charge`。    
  ***注意：如有多个装饰器，`apiview_charge` 应当放到最下面。***     
  ```python
  from onlyuserclient.decorator import apiview_charge
  class DemoViewSet(viewsets.ViewSet):
      # 参见1.3.中说明
      application_service=False

      @action(
          detail=True, 
          methods=['post'],
          url_name='bill-postpay',
          url_path='bill-postpay'
      )
      @apiview_charge(
          # 配置项 `SERVICE_ITEMS` 中的KEY
          service_key='insurance',
          # 方法调用前需要计费检查
          before=True,
          # 方法调用后需要提交计费结果
          after=True,
          # 方法调用前的计费检查只检查服务可用否，`before` 是 `True` 时有效
          usable=True,
          # 参见1.3.中说明
          application_service=False
      )
      def bill_postpay(self, request, pk=None):
          data = {
              'code': 1,
              'result': 'this is demo bill_postpay.'
          }
          return Response(data)
  ```

## API 参考
### `onlyuserclient.api.onlyuserapi` 实例对象
`onlyuserapi` 是 `simple_rest_client.api.API` 的实例对象，将一系列 onlyuser api 接口封装为实例方法。   
+ `onlyuserapi.apply_application(application, user, organization=None)`    
属于计费类接口方法，检查用户是否可以访问应用程序。即：用户或用户所在组织关联的计费账号开通了相关应用程序服务项目，项目在启用状态，计费账户状态符合条件。    
参数：       
  * `application`     
  应用程序ID     
  * `user`     
  登录用户ID      
  * `organization`    
  当前组织ID           
返回值：            

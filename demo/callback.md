# 回拨呼叫计费实现
### 分析
&emsp;&emsp;**假设**，回拨呼叫的过程：1、座席点击呼叫按键，浏览器通过 http API 向后端通信管理服务提交呼叫请求；2、通信管理服务接收到呼叫请求后根据相关设置向第三方回拨平台发起呼叫请求；3、第三方回拨平台发起通话；4、通话结束后第三方回拨平台通过 http API 回调接口向话单管理服务回传话单；5、话单管理服务接收话单并保存。    
&emsp;&emsp;**计费实现关键点**，1、能够根据计费帐户是否开通服务、帐户余额等控制座席发起呼叫请求；2、根据话单信息向计费系统提交计费请求，扣减计费帐户余额、累计通话时长等。    
### 代码实现
#### 回拨请求时控制呼叫
&emsp;&emsp;在通信管理服务项目中通过拦截 API 接口调用来控制座席回拨请求。     
```python
# settings.py
# 项目配置文件中添加配置项，详细要求请参考readme.md说明。
  MIDDLEWARE = [
      '....',
      # 计费控制中间件
      'onlyuserclient.middleware.BillingMiddleware',
  ]  

  BILLINGCLIENT = {
      '....',
      # 此项目提供的服务项目列表
      'SERVICE_ITEMS': {
          'callback': ('计费服务项目标签', '回拨呼叫', None),
      },
      '....'
  }

```
```python
# callbackview.py (假设文件名)
# 视图中在回拨接口对应方法上添加计费控制装饰器
from onlyuserclient.decorator import apiview_charge

# 假设类名
CallBackViewSet(viewsets.ViewSet):
    application_service=False

    @apiview_charge(
    # 配置项 `SERVICE_ITEMS` 中的KEY
    service_key='callback',
    # 方法调用前需要计费检查
    before=True,
    # 方法调用后需要提交计费结果
    after=False,
    # 方法调用前的计费检查只检查服务可用否，`before` 是 `True` 时有效
    usable=True
    )
    def callback(self, request, pk=None):
        ...
        return Response()

```
### 回传话单时提交计费请求    
&emsp;&emsp;在话单管理服务项目中，当接收到话单回调请求时，在处理完话单后，通过计费接口向计费系统提交计费请求，以实现回拨呼叫计费。**建议在话单表中增加“呼叫类型”和“计费成功”两个字段，以标识通话是回拨、直呼、软电话等和是否成功提交计费。方便在系统故障时恢复计费。**
```python
# settings.py 中配置参考readme.md。

# cdrview.py (假设文件名)
from onlyuserclient.api import onlyuserapi
from onlyuserclient.grpc.billing.counter import CounterClient

# 计费gRPC服务地址， 建议在setting.py中添加环境变量配置项，方便修改。
BILL_GRPC_ADDR = 'grpc.billing:50080'

# 假设类名
CdrViewSet(viewsets.ViewSet):
    def cdr(self, request, pk=None):
        # 这里处理保存话单
        
        #下面计费处理
        # 根据话单中 organization_id 查询计费帐号。这里建议用django database cache 缓存计费帐号，可以大幅减少重复调用，但要控制好TTL，减少计费帐号绑定修改后计费错误，建议60秒。
        accno = get_organization_billaccount(organization_id)
        
        client = CounterClient(BILL_GRPC_ADDR)

        try:
            client.end_service(
                # 取上面返回计费帐号
                accno, 
                # 从settings.py中取得回拨计费项目标签, 详见readme.md 1.3 
                label, 
                # 取话单中uuid字段, 如果没有可以用objectid生成
                providerno, 
                # 取话单中应答时间
                start_time, 
                # 取话单中挂机时间
                finish_time=None, 
                count=1, 
                # 取话单中关键字段和accno格式化一个字符串，便于理解。
                summary='...', 
                # 取话单中 organization_id
                organization=None
            )

            # 设置话单“计费成功”标志为 'True'

        except:
            # 计费提交不成功。在话单管理项目中可以增加定时程序对“计费成功”标志为 'False' 的话单重新提交。
            pass

        ....
```

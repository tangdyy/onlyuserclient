import json
import grpc
import atexit
from onlyuserclient.grpc.billing.proto import counter_pb2
from onlyuserclient.grpc.billing.proto import counter_pb2_grpc

# 默认计费服务器 gRPC 地址
DEFAULT_GRPC_ADDRESS = 'localhost:50051'
# 默认服务器最大重连次数
DEFAULT_MAX_RETRES = 5
# 默认最长退出时间
DEFAULT_MAX_BACKOFF = '5s'
# 域名解析超时(ms)
DEFAULT_DNS_TIMEOUT = 5000

# 个人帐户
ACCOUNT_KIND_PERSONAL = counter_pb2.CreateAccountRequest.PS
# 公司帐户
ACCOUNT_KIND_COMPANY = counter_pb2.CreateAccountRequest.CO


class CounterClient():
    '''计费应用程序 gRPC 客户端 
    '''
    def __init__(
        self, 
        server=None,
        max_retres=None, 
        max_backoff=None
        ):
        """计费应用程序 gRPC 客户端 

        Args:
            server (string, optional): 计费服务器 gRPC 地址. 默认 :50080.
            max_retres (int, optional): 最大重连次数 2-5, 0 不重连. 默认 0.
            max_backoff (string, optional): 最长退出时间. 默认 5s.
        """
        self._server_addr = server or DEFAULT_GRPC_ADDRESS
        self._max_retres = max_retres or DEFAULT_MAX_RETRES
        self._max_backoff = max_backoff or DEFAULT_MAX_BACKOFF
        options = []
        if self._max_retres > 0:
            options.append(("grpc.enable_retries", 1))                    
            service_config_json = json.dumps({
                "methodConfig": [{
                    # To apply retry to all methods, put [{}] in the "name" field
                    "name": [{}],
                    "retryPolicy": {
                        "maxAttempts": self._max_retres,
                        "initialBackoff": "0.1s",
                        "maxBackoff": self._max_backoff,
                        "backoffMultiplier": 2,
                        "retryableStatusCodes": ["UNAVAILABLE"],
                    },
                }]
            })
            options.append(("grpc.service_config", service_config_json))
        else:
            options.append(("grpc.enable_retries", 0)) 
            
        self._channel = grpc.insecure_channel(self._server_addr, options=options)
        self._stub = counter_pb2_grpc.CounterServiceStub(self._channel)
        atexit.register(self.close)

    def close(self):
        print('exit and close')
        self._channel.stop()

    def create_account(
        self, 
        owner, 
        kind, 
        name
        ):
        """创建计费帐户

        Args:
            owner (string): 帐户关联的用户ID
            kind (string): 帐户类别 
            name (string): 帐户名称 
        """  
        assert kind in (ACCOUNT_KIND_PERSONAL, ACCOUNT_KIND_COMPANY)   
        request = counter_pb2.CreateAccountRequest(
            owner=owner,
            kind=kind,
            name=name
        )
        return self._stub.CreateAccount(request)

    def query_account(
        self, 
        userid=None, 
        applicationid=None, 
        organizationid=None
        ):
        """查询计费帐户

        Args:
            userid (string, optional): 用户ID. 默认 None.
            applicationid (string, optional): 应用ID. 默认 None.
            organizationid (string, optional): 组织ID. 默认 None.
        """        
        assert userid or (applicationid and organizationid)
        request = counter_pb2.QueryAccountRequest(
            userid=userid,
            applicationid=applicationid,
            organizationid=organizationid
        )
        return self._stub.QueryAccount(request)

    def usable_service(
        self, 
        accno, 
        label, 
        count=1
        ):
        """检查服务可用

        Args:
            accno (string): 计费帐号
            label (string): 服务项目标签
            count (int, optional): 数量. 默认值 1.
        """
        assert accno and label
        request = counter_pb2.UsableServiceRequest(
            accno=accno,
            label=label,
            count=count
        ) 
        res = self._stub.UsableService(request)     
        return res.usable

    def start_service(
        self, 
        accno,
        label,        
        providerno,
        start_time=None,
        count=1,
        summary=None,
        application=None,
        organization=None,
        expire=None,
        usable=False
        ):
        """开始服务计费

        Args:
            accno (string): 计费帐号
            label (string): 服务项目标签
            providerno (string): 服务方序列号
            start_time (datetime, optional): 服务开始时间. 默认值 None.
            count (int, optional): 数量. 默认值 1.
            summary (string, optional): 摘要. 默认值 None.
            application (string, optional): 应用程序ID. 默认值 None.
            organization (string, optional): 组织ID. 默认值 None.
            expire (datetime, optional): 超时时间. 默认值 None.
            usable (bool, optional): 是否只检查服务可用. 默认值 False.
        """    
        assert accno and label
        request = counter_pb2.StartServiceRequest(
            accno=accno,
            label=label,        
            providerno=providerno,
            start_time=start_time.isoformat() if start_time else None,
            count=count,
            summary=summary,
            application=application,
            organization=organization,
            expire=expire.isoformat() if expire else None,
            usable=usable           
        )
        return self._stub.StartService(request)

    def end_service(
        self, 
        accno,
        label,        
        providerno,
        start_time,
        svcno=None,
        finish_time=None,
        count=1,
        summary=None,
        application=None,
        organization=None
        ):
        """结束服务计费

        Args:
            accno (string): 计费帐号            
            label (string): 服务项目标签
            providerno (string): 服务方序列号
            start_time (datetime): 服务开始时间
            svcno (string): 服务流水号. 默认 None.
            finish_time (datetime, optional): 服务结束时间. 默认值 None.
            count (int, optional): 数量. 默认值 1.
            summary (string, optional): 摘要. 默认值 None.
            application (string, optional): 应用程序ID. 默认值 None.
            organization (string, optional): 组织ID. 默认值 None.
        """        
        assert accno and label and providerno
        request = counter_pb2.EndServiceRequest(
            accno=accno,
            svcno=svcno,
            label=label,        
            providerno=providerno,
            start_time=start_time.isoformat() if start_time else None,
            finish_time=finish_time.isoformat() if finish_time else None,
            count=count,
            summary=summary,
            application=application,
            organization=organization
        )
        return self._stub.EndService(request)

    def increase_resource(
        self,
        accno,
        label,
        count=1,
        total=None
        ):
        """增加资源占用

        Args:
            accno (string): 计费帐号
            label (string): 服务项目标签
            count (int, optional): 新增占用资源数量. 默认 1.
            total (int, optional): 占用资源总数. 默认 None.
        """
        assert accno and label
        request = counter_pb2.ResourceRequest(
            accno=accno,
            label=label,
            count=count,
            total=total
        )
        self._stub.IncreaseResource(request)
        
    def reduce_resource(
        self,
        accno,
        label,
        count=1,
        total=None
        ):
        """减少资源占用

        Args:
            accno (string): 计费帐号
            label (string): 服务项目标签
            count (int, optional): 减少占用资源数量. 默认 1.
            total (int, optional): 占用资源总数. 默认 None.
        """
        assert accno and label
        request = counter_pb2.ResourceRequest(
            accno=accno,
            label=label,
            count=count,
            total=total
        )
        self._stub.ReduceResource(request)
        
    def keep_service(
        self,
        accno,
        label,
        providerno=None,
        expire=None
        ):
        """服务计费保持

        Args:
            accno (string): 计费帐号
            label (string): 服务项目标签
            providerno (string, optional): 服务序列号. 默认 None.
            expire (datetime, optional): 服务超时时间. 默认 None.
        """
        assert accno and label
        request = counter_pb2.KeepServiceRequest(
            accno=accno,
            label=label,
            providerno=providerno,
            expire=expire.isoformat() if expire else None
        )
        self._stub.KeepService(request)
    
    def query_account_service(
        self,
        accno,
        label
        ):
        """查询计费帐户服务可用

        Args:
            accno (string): 计费帐号
            label (string): 服务项目标签
        """        
        assert accno and label
        request = counter_pb2.QueryAccountServiceRequest(
            accno=accno,
            label=label            
        ) 
        res = self._stub.QueryAccountService(request)
        code = res.code or -1
        detail = res.detail or ''
        return code, detail
    
    def query_subaccounts(
        self,
        parent,
        label=None
        ):
        """查询子帐户

        Args:
            parent (string): 主帐户帐号
            label (string, 计费服务项目标签): 如果此参数不是 None ,只返回开通服务项目的帐号列表, 包括主帐号. 默认 None.
        """
        assert parent
        request = counter_pb2.QuerySubAccountRequest(
            parent=parent,
            label=label
        )
        response = self._stub.QuerySubAccount(request)
        return response.accounts or []
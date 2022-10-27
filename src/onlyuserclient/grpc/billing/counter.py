import time
import grpc
from onlyuserclient.grpc.billing.proto import counter_pb2
from onlyuserclient.grpc.billing.proto import counter_pb2_grpc

# 默认计费服务器 gRPC 地址
DEFAULT_GRPC_ADDRESS = 'localhost:50080'
# 默认服务器最大重连次数
DEFAULT_MAX_RECONNECT = 0
# 默认重连间隔时间(秒)
DEFAULT_RECONNECT_INTERVAL = 5

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
        max_reconnect=DEFAULT_MAX_RECONNECT, 
        reconnect_interval=DEFAULT_RECONNECT_INTERVAL
        ):
        """计费应用程序 gRPC 客户端 

        Args:
            server (string, optional): 计费服务器 gRPC 地址. 默认 :50080.
            max_reconnect (int, optional): 最大重连次数. 默认 0.
            reconnect_interval (int, optional): 重连间隔时间(秒). 默认 5.
        """
        self._server_addr = server or DEFAULT_GRPC_ADDRESS
        self._max_reconnect = max_reconnect
        self._reconnect_interval = reconnect_interval

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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.CreateAccount(request)
            channel.close()
        return res

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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.QueryAccount(request)
            channel.close()
        return res

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
        usable = False
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.UsableService(request)     
            usable = res.usable
            channel.close()
        return usable

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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.StartService(request)
            channel.close()
        return res

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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.EndService(request)
            channel.close()
        return res
    
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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.IncreaseResource(request)
            channel.close()
        return res
        
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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.ReduceResource(request)
            channel.close()
        return res
        
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
        res = None
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)
            res = stub.KeepService(request)
            channel.close()
        return res
    
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
        code = -1
        detail = ''
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)       
            res = stub.QueryAccountService(request)
            code = res.code
            detail = res.detail
            channel.close()
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
        accounts = []
        with grpc.insecure_channel(self._server_addr) as channel:
            stub = counter_pb2_grpc.CounterServiceStub(channel)   
            response = stub.QuerySubAccount(request)
            accounts = response.accounts
            channel.close()
        return accounts
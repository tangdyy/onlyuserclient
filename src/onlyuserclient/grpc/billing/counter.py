import time
from httpx import request
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
        addr = server or DEFAULT_GRPC_ADDRESS
        self._max_reconnect = max_reconnect
        self._reconnect_interval = reconnect_interval
        channel = grpc.insecure_channel(addr)
        self._stub = counter_pb2_grpc.CounterServiceStub(channel)

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
        response = self._stub.UsableService(request)     
        return response.usable

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
        retry = self._max_reconnect
        while True:             
            exec = None
            try:
                response = self._stub.EndService(request)
            except Exception as e:
                exec = e

            if exec and exec.code() == grpc.StatusCode.UNAVAILABLE and retry > 0:
                retry -= 1
                time.sleep(self._reconnect_interval)
                continue
            if exec:
                raise exec
            break
        return response
    
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
        return self._stub.IncreaseResource(request)

        
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
        return self._stub.ReduceResource(request)
        
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
        return self._stub.KeepService(request)
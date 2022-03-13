import grpc
from grpc.billing.proto import counter_pb2
from grpc.billing.proto import counter_pb2_grpc
from onlyuserclient.settings import billing_settings

class CounterClient():
    '''计费应用程序 gRPC 客户端 
    '''
    def __init__(self, server=None):
        """计费应用程序 gRPC 客户端 

        Args:
            server (string, optional): 计费服务器 gRPC 地址. 默认 :50080.
        """
        addr = server or billing_settings.GRPC_ADDRESS
        channel = grpc.insecure_channel(addr)
        self._stub = counter_pb2_grpc.CounterServiceStub(channel)

    def create_account(self, owner, kind, name):
        """创建计费帐户

        Args:
            owner (string): 帐户关联的用户ID
            kind (string): 帐户类别 
            name (string): 帐户名称 
        """     
        request = counter_pb2.CreateAccountRequest(
            owner=owner,
            kind=kind,
            name=name
        )
        response = self._stub.CreateAccount(request)
        return response.message
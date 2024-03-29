# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import counter_pb2 as counter__pb2


class CounterServiceStub(object):
    """面向应用程序的服务接口
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateAccount = channel.unary_unary(
                '/counter.CounterService/CreateAccount',
                request_serializer=counter__pb2.CreateAccountRequest.SerializeToString,
                response_deserializer=counter__pb2.AccountResponse.FromString,
                )
        self.QueryAccount = channel.unary_unary(
                '/counter.CounterService/QueryAccount',
                request_serializer=counter__pb2.QueryAccountRequest.SerializeToString,
                response_deserializer=counter__pb2.AccountResponse.FromString,
                )
        self.UsableService = channel.unary_unary(
                '/counter.CounterService/UsableService',
                request_serializer=counter__pb2.UsableServiceRequest.SerializeToString,
                response_deserializer=counter__pb2.UsableServiceResponse.FromString,
                )
        self.StartService = channel.unary_unary(
                '/counter.CounterService/StartService',
                request_serializer=counter__pb2.StartServiceRequest.SerializeToString,
                response_deserializer=counter__pb2.StartServiceResponse.FromString,
                )
        self.EndService = channel.unary_unary(
                '/counter.CounterService/EndService',
                request_serializer=counter__pb2.EndServiceRequest.SerializeToString,
                response_deserializer=counter__pb2.EndServiceResponse.FromString,
                )
        self.IncreaseResource = channel.unary_unary(
                '/counter.CounterService/IncreaseResource',
                request_serializer=counter__pb2.ResourceRequest.SerializeToString,
                response_deserializer=counter__pb2.ResourceResponse.FromString,
                )
        self.ReduceResource = channel.unary_unary(
                '/counter.CounterService/ReduceResource',
                request_serializer=counter__pb2.ResourceRequest.SerializeToString,
                response_deserializer=counter__pb2.ResourceResponse.FromString,
                )
        self.KeepService = channel.unary_unary(
                '/counter.CounterService/KeepService',
                request_serializer=counter__pb2.KeepServiceRequest.SerializeToString,
                response_deserializer=counter__pb2.KeepServiceResponse.FromString,
                )
        self.QueryAccountService = channel.unary_unary(
                '/counter.CounterService/QueryAccountService',
                request_serializer=counter__pb2.QueryAccountServiceRequest.SerializeToString,
                response_deserializer=counter__pb2.QueryAccountServiceResponse.FromString,
                )
        self.QuerySubAccount = channel.unary_unary(
                '/counter.CounterService/QuerySubAccount',
                request_serializer=counter__pb2.QuerySubAccountRequest.SerializeToString,
                response_deserializer=counter__pb2.QuerySubAccountResponse.FromString,
                )


class CounterServiceServicer(object):
    """面向应用程序的服务接口
    """

    def CreateAccount(self, request, context):
        """创建计费帐户
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryAccount(self, request, context):
        """查询计费帐户
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UsableService(self, request, context):
        """检查服务可用
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartService(self, request, context):
        """开始服务计费
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EndService(self, request, context):
        """结束服务计费
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IncreaseResource(self, request, context):
        """增加资源占用
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReduceResource(self, request, context):
        """减少资源占用
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def KeepService(self, request, context):
        """保持服务计费
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryAccountService(self, request, context):
        """查询计费帐户服务项目可用
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySubAccount(self, request, context):
        """查询子帐户
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CounterServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccount,
                    request_deserializer=counter__pb2.CreateAccountRequest.FromString,
                    response_serializer=counter__pb2.AccountResponse.SerializeToString,
            ),
            'QueryAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryAccount,
                    request_deserializer=counter__pb2.QueryAccountRequest.FromString,
                    response_serializer=counter__pb2.AccountResponse.SerializeToString,
            ),
            'UsableService': grpc.unary_unary_rpc_method_handler(
                    servicer.UsableService,
                    request_deserializer=counter__pb2.UsableServiceRequest.FromString,
                    response_serializer=counter__pb2.UsableServiceResponse.SerializeToString,
            ),
            'StartService': grpc.unary_unary_rpc_method_handler(
                    servicer.StartService,
                    request_deserializer=counter__pb2.StartServiceRequest.FromString,
                    response_serializer=counter__pb2.StartServiceResponse.SerializeToString,
            ),
            'EndService': grpc.unary_unary_rpc_method_handler(
                    servicer.EndService,
                    request_deserializer=counter__pb2.EndServiceRequest.FromString,
                    response_serializer=counter__pb2.EndServiceResponse.SerializeToString,
            ),
            'IncreaseResource': grpc.unary_unary_rpc_method_handler(
                    servicer.IncreaseResource,
                    request_deserializer=counter__pb2.ResourceRequest.FromString,
                    response_serializer=counter__pb2.ResourceResponse.SerializeToString,
            ),
            'ReduceResource': grpc.unary_unary_rpc_method_handler(
                    servicer.ReduceResource,
                    request_deserializer=counter__pb2.ResourceRequest.FromString,
                    response_serializer=counter__pb2.ResourceResponse.SerializeToString,
            ),
            'KeepService': grpc.unary_unary_rpc_method_handler(
                    servicer.KeepService,
                    request_deserializer=counter__pb2.KeepServiceRequest.FromString,
                    response_serializer=counter__pb2.KeepServiceResponse.SerializeToString,
            ),
            'QueryAccountService': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryAccountService,
                    request_deserializer=counter__pb2.QueryAccountServiceRequest.FromString,
                    response_serializer=counter__pb2.QueryAccountServiceResponse.SerializeToString,
            ),
            'QuerySubAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.QuerySubAccount,
                    request_deserializer=counter__pb2.QuerySubAccountRequest.FromString,
                    response_serializer=counter__pb2.QuerySubAccountResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'counter.CounterService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CounterService(object):
    """面向应用程序的服务接口
    """

    @staticmethod
    def CreateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/CreateAccount',
            counter__pb2.CreateAccountRequest.SerializeToString,
            counter__pb2.AccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/QueryAccount',
            counter__pb2.QueryAccountRequest.SerializeToString,
            counter__pb2.AccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UsableService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/UsableService',
            counter__pb2.UsableServiceRequest.SerializeToString,
            counter__pb2.UsableServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/StartService',
            counter__pb2.StartServiceRequest.SerializeToString,
            counter__pb2.StartServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EndService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/EndService',
            counter__pb2.EndServiceRequest.SerializeToString,
            counter__pb2.EndServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IncreaseResource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/IncreaseResource',
            counter__pb2.ResourceRequest.SerializeToString,
            counter__pb2.ResourceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReduceResource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/ReduceResource',
            counter__pb2.ResourceRequest.SerializeToString,
            counter__pb2.ResourceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def KeepService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/KeepService',
            counter__pb2.KeepServiceRequest.SerializeToString,
            counter__pb2.KeepServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryAccountService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/QueryAccountService',
            counter__pb2.QueryAccountServiceRequest.SerializeToString,
            counter__pb2.QueryAccountServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySubAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/counter.CounterService/QuerySubAccount',
            counter__pb2.QuerySubAccountRequest.SerializeToString,
            counter__pb2.QuerySubAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

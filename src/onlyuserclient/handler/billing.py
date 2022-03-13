import importlib
from django.utils import timezone
from django.http import HttpRequest
from rest_framework.request import Request
from onlyuserclient import exceptions
from onlyuserclient.settings import billing_settings
from onlyuserclient.utils import functions
from onlyuserclient.api import billingapi
from onlyuserclient.api import onlyuserapi

__all__ = (
    'BillApiHandler',
    'get_billapi_handler'
)


class BillApiHandler():
    '''Api计费处理
    '''
    def __init__(
        self,
        service_label,
        service_name=None,
        before=True,
        after=True,
        usable=True,
        application_service=False,
        fun_name=None,
        fun_doc=None
        ):
        self.service_label = service_label 
        self.service_name = service_name
        self.before = before
        self.after = after
        self.usable = usable
        self.application_service = application_service
        self.fun_name = fun_name
        self.fun_doc = fun_doc

    def _get_user_id(self, request):
        return request.headers.get('X-User-Id', None)

    def _get_application_id(self, request):
        return request.headers.get('X-Application-Id', None) 

    def _get_current_org_id(self, request):
        return request.headers.get('X-Current-Org', None)

    def _get_request(self, *args, **kwargs):
        if len(args) < 1:
            return None
        if isinstance(args[0], HttpRequest) or isinstance(args[0], Request):
            return args[0]
        if len(args) < 2:
            return None
        if isinstance(args[1], HttpRequest) or isinstance(args[1], Request):
            return args[1]
        return None        

    def get_before_count(self, request=None):
        return 1

    def get_after_count(self, request, response, before_count=1):
        return before_count

    def get_before_start_time(self, request=None):
        return timezone.now()

    def get_after_start_time(self, request, response, before_start_time=None):
        return before_start_time

    def get_finish_time(self, request, response):
        return timezone.now()

    def get_summary(self, request, response=None):
        tpl = '服务项目：{};应用程序：{};组织/团队：{};用户：{};'
        app = self.get_application_info(request)
        org = self.get_organization_info(request)
        user = self.get_user_info(request)
        summary = tpl.format(
            self.service_name,
            app['name'] if app else '',
            org['name'] if org else '',           
            (user['username'] + ',' + user['nickname'] ) if user else ''
        )
        return summary

    def set_service_params(self, request, name, value):
        '''设置服务参数
        '''
        if not hasattr(request, '_service_params'):
            setattr(request, '_service_params', {})
        request._service_params[name] = value      
        
    def get_service_params(self, request, name=None):
        '''返回服务参数
        '''
        if not hasattr(request, '_service_params'):
            return None
        if name is None:
            return request._service_params
        return request._service_params.get(name, None)

    def get_application_info(self, request):
        '''获得请求对象的应用信息
        '''
        appid= self._get_application_id(request)
        if appid is None:
            return None
        return onlyuserapi.get_application_info(appid)

    def get_organization_info(self, request):
        '''获取请求对象的组织信息
        '''
        orgid = self._get_current_org_id(request)
        if orgid is None:
            return None
        return onlyuserapi.get_organization_info(orgid)

    def get_user_info(self, request):
        '''获取请求对象的用户信息
        '''
        userid = self._get_user_id(request)
        if userid is None:
            return None
        return onlyuserapi.get_user_info(userid)

    def get_accno_by_organization(self, request):
        '''获取组织绑定的计费账号
        '''
        org_id = self._get_current_org_id(request)
        if org_id is None:
            return None
        return onlyuserapi.get_organization_billaccount(org_id)

    def get_accno_by_user(self, request):
        '''获取用户的计费账号
        '''
        user_id = self._get_user_id(request)
        if user_id is None:
            return None
        return billingapi.get_account_by_user(user_id)

    def request_service(self, request):
        '''请求开始服务计费
        '''
        accno = self.get_service_params(request, 'accno')
        providerno = self.get_service_params(request, 'providerno')
        label = self.get_service_params(request, 'label')
        start_time = self.get_service_params(request, 'start_time')
        count = self.get_service_params(request, 'count')
        summary = self.get_service_params(request, 'summary')
        application = self.get_service_params(request, 'application')
        organization = self.get_service_params(request, 'organization')  

        svcno = None
        if accno:      
            svcno, expire = billingapi.request_service(
                accno,
                providerno, 
                label,
                start_time,
                count,        
                summary,
                application,
                organization
            )
        if svcno is None:
            raise exceptions.ServiceForbidden(
                application,
                organization,
                self.get_service_params(request, 'user'),
                label
            )
        self.set_service_params(request, 'svcno', svcno)

    def finish_service(self, request, response):
        '''结束服务计费
        '''
        if response.status_code < 200 or response.status_code >= 300:
            return
        accno = self.get_service_params(request, 'accno')
        providerno = self.get_service_params(request, 'providerno')
        label = self.get_service_params(request, 'label')
        start_time = self.get_service_params(request, 'start_time')
        count = self.get_service_params(request, 'count')
        summary = self.get_service_params(request, 'summary')
        application = self.get_service_params(request, 'application')
        organization = self.get_service_params(request, 'organization')    
        finish_time = self.get_service_params(request, 'finish_time')
        svcno = self.get_service_params(request, 'svcno')    
        billingapi.finished_service(
            accno,
            providerno,
            label,
            start_time,
            finish_time,
            count,        
            summary,
            application,
            organization,
            svcno
        )

    def usable_service(self, request):
        '''检查
        '''
        accno = self.get_service_params(request, 'accno')
        label = self.get_service_params(request, 'label')
        count = self.get_service_params(request, 'count')
        usable = False
        if accno:
            usable = billingapi.usable_service(accno, label, count)
        if not usable:
            raise exceptions.ServiceForbidden(
                self.get_service_params(request, 'application'),
                self.get_service_params(request, 'organization'),
                self.get_service_params(request, 'user'),
                label
            )            

    def apply_application(self, request):
        '''检查应用是否计费可用
        '''
        application = self.get_service_params(request, 'application')
        organization = self.get_service_params(request, 'organization')
        user = self.get_service_params(request, 'user')
        code = -1
        if application and organization and user:
            code, detail = onlyuserapi.apply_application(
                application, 
                user, 
                organization
            )
        setattr(request, '_application_check', True)
        if code != 0:
            raise exceptions.ApplicationForbidden(
                application, 
                user, 
                organization,
                detail
            )

    def before_api(self, *args, **kwargs):
        '''API调用前
        '''
        request = self._get_request(*args, **kwargs)
        self.set_service_params(request, 'accno', self.get_accno_by_organization(request))
        self.set_service_params(request, 'application', self._get_application_id(request))
        self.set_service_params(request, 'organization', self._get_current_org_id(request))
        self.set_service_params(request, 'user', self._get_user_id(request))
        self.set_service_params(request, 'providerno', functions.generate_serial_number(self.fun_name[:4]))
        self.set_service_params(request, 'count', self.get_before_count(request))
        self.set_service_params(request, 'start_time', self.get_before_start_time(request))
        self.set_service_params(request, 'label', self.service_label)   
        self.set_service_params(request, 'summary', self.get_summary(request))

        if self.application_service and not request._application_check:
            self.apply_application(request)

        if not self.before:
            return 

        if self.usable:
            self.usable_service(request)
        else:
            self.request_service(request)        

    def after_api(self, response, *args, **kwargs):
        '''API调用后
        '''
        request = self._get_request(*args, **kwargs)
        before_count = self.get_before_count(request)
        before_start_time = self.get_before_start_time(request)
        self.set_service_params(
            request, 
            'count', 
            self.get_after_count(request, response, before_count)
        )
        self.set_service_params(
            request, 
            'start_time', 
            self.get_after_start_time(request, response, before_start_time)
        )  
        self.set_service_params(
            request,
            'finish_time',
            self.get_finish_time(request, response)
        )  
        self.set_service_params(
            request,
            'summary',
            self.get_summary(request, response)
        )    
        self.finish_service(request, response)



def get_billapi_handler(
    service_key,
    before=True,
    after=True,
    usable=True,
    application_service=False
    ):
    '''返回一个API接口计费处理器对象.
    '''
    service_item = billing_settings.SERVICE_ITEMS.get(service_key, None)
    if service_item is None:
        raise ValueError('The service key is not a valid value.')
     
    if len(service_item) < 3:
        raise ValueError('settings BILLING.SERVICE_ITEMS key: %s error.'%(service_key,))
    
    service_label = service_item[0]
    service_name = service_item[1] or service_label
    bill_handler_module =  service_item[2]    
    bill_handler_cls = None
    if bill_handler_module:
        arr = bill_handler_module.split('.')
        module_name = '.'.join(arr[:-1])
        cls_name = arr[-1:][0]
        module = importlib.import_module(module_name)
        bill_handler_cls = getattr(module, cls_name, None)
        if bill_handler_cls is None:
            raise ValueError('The service itme handler is not valid value.')
    else:
        bill_handler_cls = BillApiHandler

    handler = bill_handler_cls(
        service_label,
        service_name=service_name,
        before=before,
        after=after,
        usable=usable,
        application_service=application_service       
    ) 
    return handler
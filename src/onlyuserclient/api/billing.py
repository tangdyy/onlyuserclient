import datetime
from rest_framework.exceptions import APIException
from simple_rest_client.resource import Resource
from simple_rest_client import exceptions
from django.utils import timezone
from .base import BaseAPI
from onlyuserclient.settings import billing_settings
from onlyuserclient.utils import functions

__all__ = ('billingapi', )


CACHE_API = billing_settings.CACHE_API
CACHE_TTL = billing_settings.CACHE_TTL
dbcache = functions.get_bill_cache()


class BillingFail(APIException):
    '''计费失败
    '''
    status_code = 403
    default_detail = '计费失败,拒绝服务.'
    default_code = 'billing_fail'    
    def __init__(self, exec=None):
        super().__init__()
        self.code = -1
        response = getattr(exec, 'response', None)
        if response:
            self.status_code = response.status_code
            self.code = response.body.get('code', -1)
            msg = response.body.get('detail', None)
            if msg is None:
                msg = response.body.get('non_field_errors', None)

            self.detail = {
                'detail': msg or self.default_detail
            }


class BillAccountNotExist(APIException):
    '''没有绑定计费账户
    '''
    status_code = 404
    default_detail = '没有绑定计费账户.'
    default_code = 'account_not_exist'    
    def __init__(self, detail=None):
        super().__init__()
        self.detail = {
            'detail': detail or self.default_detail,
        }


class BillAccountResource(Resource):
    '''计费接口资源定义
    '''
    actions = {
        "retrieve": {'method': 'GET', 'url': '/api/billaccounts/{}/'}, 
        "list": {'method': 'GET', 'url': '/api/billaccounts/'},
        "request_service": {'method': 'POST', 'url': '/api/billaccounts/{}/request-service/'},
        "finished_service": {'method': 'POST', 'url': '/api/billaccounts/{}/finished-service/'},
        "increase_resource": {'method': 'POST', 'url': '/api/billaccounts/{}/increase-resource/'},
        "reduce_resource": {'method': 'POST', 'url': '/api/billaccounts/{}/reduce-resource/'},    
        "usable_service": {'method': 'POST', 'url': '/api/billaccounts/{}/usable-service/'}, 
        "query_subaccounts": {'method': 'GET', 'url': '/api/billaccounts/{}/query-subaccounts/'}    
    }


class BillingApi(BaseAPI):
    '''计费接口
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_resource(resource_name='accounts', resource_class=BillAccountResource)

    def get_account_by_user(self, userid):
        '''返回用户个人计费账号
        '''
        accno = None
        ckey = functions.generate_cache_key(
            'BAPIGA',
            userid
        )
        if CACHE_API:
            accno = dbcache.get(ckey)
            if accno:
                return accno 
        
        try:
            response = self.accounts.list(params={'userid': userid})
            accno = response.body.get('number', None)
        except:
            accno = None
            pass
        if accno is None:
            raise BillAccountNotExist()
        if CACHE_API and accno is not None:
            dbcache.set(ckey, accno, CACHE_TTL)
        return accno        

    def request_service(
        self,       
        accno,
        providerno, 
        label,
        start_time=None,
        count=1,        
        summary=None,
        application=None,
        organization=None,
        expire=None
        ):
        '''请求资源使用
        ''' 
        if accno is None or providerno is None or label is None:
            raise BillingFail()
                           
        if start_time is None:
            start_time = timezone.localtime()
        start_time = start_time.astimezone(timezone.utc)
        if expire is not None:
            expire = expire.astimezone(timezone.utc)

        data = {
            'providerno': providerno,
            'label': label,
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count,            
            'summary': summary,
            'application': application,
            'organization': organization,
            'expire': expire.strftime('%Y-%m-%d %H:%M:%S') if expire else None
        }
        svcno = None
        try:
            response = self.accounts.request_service(accno, body=data)
            svcno = response.body.get('svcno', None)
            expire = response.body.get('expire', None)
        except exceptions.ClientError as e:
            raise BillingFail(e)
        try:
            ndt = datetime.datetime.strptime(
                expire, 
                '%Y-%m-%d %H:%M:%S'
            )
            adt = timezone.make_aware(ndt, timezone.utc)
        except:
            adt = None
        return svcno, adt              

    def finished_service(
        self,         
        accno,
        providerno,
        label,
        start_time,
        finish_time,
        count=1,        
        summary=None,
        application=None,
        organization=None,
        svcno=None, 
        ):
        '''资源使用完成
        ''' 
        if accno is None or providerno is None or label is None:
            raise BillingFail()

        if start_time is None:
            start_time = timezone.now()
        start_time = start_time.astimezone(timezone.utc)

        if finish_time is not None:
            finish_time = finish_time.astimezone(timezone.utc)

        data = {
            'label': label,
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_time': finish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count,
            'providerno': providerno,
            'summary': summary,
            'application': application,
            'organization': organization,
            'svcno': svcno
        }
        result = None
        try:
            response = self.accounts.finished_service(accno, body=data)
            result = response.body
        except exceptions.ClientError as e:
            raise BillingFail(e)
        return result         

    def increase_resource(self, accno, label, count=1, total=None):
        '''增加资源占用
        ''' 
        data = {
            'label': label,
            'count':  count,
            'total': total
        }   
        result = None
        try:
            response = self.accounts.increase_resource(accno, body=data)
            result = response.body
        except exceptions.ClientError as e:
            raise BillingFail(e)
        return result         

    def reduce_resource(self, accno, label, count=1, total=None):
        '''减少资源占用
        '''
        data = {
            'label': label,
            'count':  count,
            'total': total
        }   
        result = None
        try:
            response = self.accounts.reduce_resource(accno, body=data)
            result = response.body
        except exceptions.ClientError as e:
            raise BillingFail(e)
        return result                 

    def usable_service(
        self, 
        accno, 
        label,
        count=1
        ):
        '''请求资源使用
        '''        
        data = {
            'label': label,
            'count': count
        }
        usable = False
        try:
            response = self.accounts.usable_service(accno, body=data)
            usable = response.body.get('usable', False)
        except exceptions.ClientError as e:
            raise BillingFail(e)
        return usable  

    def query_subaccounts(self, parent, label=None):
        '''查询子帐户
        '''
        accounts = []
        ckey = functions.generate_cache_key(
            'BAPIQSA',
            parent
        )
        if CACHE_API:
            accounts = dbcache.get(ckey)
            if accounts is not None:
                return accounts 
        
        try:
            params = {}
            if label:
                params['label'] = label
            response = self.accounts.query_subaccounts(parent, params=params)
            accounts = response.body.get('accounts', [])
        except exceptions.ClientError as e:
            raise BillingFail(e)
            
        if CACHE_API and accounts:
            dbcache.set(ckey, accounts, CACHE_TTL)
        return accounts   
 
        
# 计费服务接口对象
billingapi = BillingApi(
    api_root_url=billing_settings.API_ROOT_URL,
    pfx=billing_settings.API_PFX,
    headers=billing_settings.API_HEADERS,
    timeout=billing_settings.API_TIMEOUT,
    apikey_header=billing_settings.APIKEY_HEADER,
    apikey=billing_settings.APIKEY    
)

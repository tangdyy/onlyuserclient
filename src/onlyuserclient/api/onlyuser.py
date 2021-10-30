import logging
from simple_rest_client.resource import Resource
from simple_rest_client.exceptions import ClientError
from onlyuserclient import exceptions
from onlyuserclient.utils import functions
from .base import BaseAPI
from onlyuserclient.settings import api_settings

__all__ =('onlyuserapi',)

logger = logging.getLogger('onlyuserclient.api.onlyuser')
CACHE_API  = api_settings.CACHE_API
CACHE_TTL = api_settings.CACHE_TTL or 60
cache = functions.get_onlyuser_cache()


class RolepermResource(Resource):
    '''角色权限访问
    '''
    actions = {
        #获得部门包含的用户ID 
        "userids_department":{'method': 'POST', 'url': '/user-role-perms/userids-department/'},
        "userids_branch":{'method': 'POST', 'url': '/user-role-perms/userids-branch/'},
        "userids_organization":{'method': 'POST', 'url': '/user-role-perms/userids-organization/'}
    }

class UserResource(Resource):
    '''用户帐号资源
    '''
    actions = {
        "retrieve":{'method': 'GET', 'url': '/users/{}/'},
    }

class OrganizationResource(Resource):
    '''组织树资源
    '''
    actions = {
        "retrieve":{'method': 'GET', 'url': '/organizations/{}/'},
        "billaccount":{'method': 'GET', 'url': '/organizations/{}/billaccount/'}, 
    }

class ApplicationResource(Resource):
    '''应用程序资源
    '''
    actions = {
        "retrieve":{'method': 'GET', 'url': '/applications/{}/'},
    }    


class BillEventResource(Resource):
    '''计费事件资源
    '''
    actions = {
        "apply_application":{'method': 'GET', 'url': '/billevents/apply-application/'},
    }    



class OnlyuserApi(BaseAPI): 
    '''Onlyuser接口
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_resource(resource_name='roleperms', resource_class=RolepermResource)
        self.add_resource(resource_name='users', resource_class=UserResource)
        self.add_resource(resource_name='organizations', resource_class=OrganizationResource)
        self.add_resource(resource_name='applications', resource_class=ApplicationResource)
        self.add_resource(resource_name='billevents', resource_class=BillEventResource)
    
    def apply_application(self, application, user, organization=None):
        '''使用应用程序
        '''
        logger.debug(
            'Call onlyuser api apply_application,'
            'application:{}, user:{}, organization:{}.'.format(
                application, user, organization
            )
        )
        if api_settings.LOCAL:
            logger.warning('Onlyuser api is local mode.')
            return 0, 'this local mode.'
        
        ckey = functions.generate_cache_key(
            'BAPIAA', 
            application, 
            user, 
            organization
        )
        if CACHE_API:
            result = cache.get(ckey)
            if result:
                return result

        params = {
            'application': application, 
            'user': user, 
            'organization': organization
        }
        code = None
        detail = None
        try:
            response = self.billevents.apply_application(params=params)
            code = response.body.get('code', None)
            detail = response.body.get('detail', None)
            if CACHE_API:
                cache.set(ckey, (code, detail), CACHE_TTL)
        except ClientError as exec:
            response = getattr(exec, 'response', None)
            if response:
                code = response.body.get('code', None)
                detail = response.body.get('detail', None)
        except:
            pass
        return code, detail

    def get_organization_billaccount(self, organization_id):
        '''查询组织绑定计费账号
        '''
        logger.debug(
            'Call onlyuser api organization billaccount,'
            'organization:{}.'.format(organization_id )
        )
        if api_settings.LOCAL:
            logger.warning('Onlyuser api is local mode.')
            return 'P00000000'        
        ckey = functions.generate_cache_key(
            'BAPIOB', 
            'organization_billaccount', 
            organization_id
        )
        if CACHE_API:
            result = cache.get(ckey)
            if result:
                return result        
        try:
            response = self.organizations.billaccount(organization_id)
            accno = response.body.get('accno', None)
            if accno and CACHE_API:
                cache.set(ckey, accno, CACHE_TTL)
        except:
            accno = None
            pass
        return accno

    def get_application_info(self, application_id):
        '''查询应用程序信息
        '''
        logger.debug(
            'Call onlyuser api application info,'
            'application:{}.'.format(application_id)
        )
        if api_settings.LOCAL:
            logger.warning('Onlyuser api is local mode.')
            data={
                'id': application_id,
                'name': 'this local model application'
            }
            return data

        ckey = functions.generate_cache_key(
            'BAPIAI', 
            'application_info', 
            application_id
        )
        if CACHE_API:
            result = cache.get(ckey)
            if result:
                return result             

        data =None
        try:
            response = self.applications.retrieve(application_id)
            data = response.body
            if CACHE_API:
                cache.set(ckey, data, CACHE_TTL)
        except:
            pass
        return data

    def get_organization_info(self, organization_id):
        '''查询组织信息
        '''
        logger.debug(
            'Call onlyuser api organization info,'
            'organization:{}.'.format(organization_id)
        )
        if api_settings.LOCAL:
            logger.warning('Onlyuser api is local mode.')
            data={
                'id': organization_id,
                'name': 'this local model organization'
            }
            return data

        ckey = functions.generate_cache_key(
            'BAPIOI', 
            'organization_info', 
            organization_id
        )
        if CACHE_API:
            result = cache.get(ckey)
            if result:
                return result             

        data =None
        try:
            response = self.organizations.retrieve(organization_id)
            data = response.body
            if CACHE_API:
                cache.set(ckey, data, CACHE_TTL)
        except:
            pass
        return data

    def get_user_info(self, user_id):
        '''查询用户信息
        '''
        logger.debug(
            'Call onlyuser api user info,'
            'user:{}.'.format(user_id)
        )
        if api_settings.LOCAL:
            logger.warning('Onlyuser api is local mode.')
            data={
                'id': user_id,
                'username': 'localuser',
                'nickname': 'local user'
            }
            return data

        ckey = functions.generate_cache_key(
            'BAPIUI', 
            'user_info', 
            user_id
        )
        if CACHE_API:
            result = cache.get(ckey)
            if result:
                return result             

        data =None
        try:
            response = self.users.retrieve(user_id)
            data = response.body
            if CACHE_API:
                cache.set(ckey, data, CACHE_TTL)
        except:
            pass
        return data


onlyuserapi = OnlyuserApi(pfx=api_settings.ONLYUSER_PFX)

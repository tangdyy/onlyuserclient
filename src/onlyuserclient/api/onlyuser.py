from simple_rest_client.resource import Resource
from .base import BaseAPI
from onlyuserclient.settings import api_settings

__all__ =('onlyuserapi',)

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
        if api_settings.LOCAL:
            return 0, 'this local mode.'
            
        params = {
            'application': application, 
            'user': user, 
            'organization': organization
        }
        try:
            response = self.billevents.apply_application(params=params)
            code = response.body.get('code', None)
            detail = response.body.get('detail', None)
        except:
            code = None
            detail = None
            pass
        return code, detail


onlyuserapi = OnlyuserApi(pfx=api_settings.ONLYUSER_PFX)

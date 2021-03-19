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

onlyuserapi = BaseAPI(pfx=api_settings.ONLYUSER_PFX)
onlyuserapi.add_resource(resource_name='roleperms', resource_class=RolepermResource)
onlyuserapi.add_resource(resource_name='users', resource_class=UserResource)
onlyuserapi.add_resource(resource_name='organizations', resource_class=OrganizationResource)

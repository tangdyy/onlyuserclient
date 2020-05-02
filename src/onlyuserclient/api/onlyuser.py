from simple_rest_client.resource import Resource
from .base import BaseAPI

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

onlyuserapi = BaseAPI()
onlyuserapi.add_resource(resource_name='roleperms', resource_class=RolepermResource)

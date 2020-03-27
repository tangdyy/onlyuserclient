from .base import BaseAPI
from simple_rest_client import exceptions
from simple_rest_client.resource import Resource
from django.conf import settings

class RolepermResource(Resource):
    '''角色权限访问
    '''
    actions = {
        "userids_department":{'method': 'POST', 'url': '/user-role-perms/userids-department/'},
        "userids_branch":{'method': 'POST', 'url': '/user-role-perms/userids-branch/'},
        "userids_organization":{'method': 'POST', 'url': '/user-role-perms/userids-organization/'}
    }


class OnlyuserApi( BaseAPI):
    '''onlyuser API
        实例化有两个初始化参数: 
        @api_root_url      onlyuser服务的地址
        @timeout           访问超时,单位秒, 默认是30
        这两件参数可以在django配置文件中设置, 配置项名称分别是`ONLYUSER_API_URL`和`API_TIMEOUT`
        ```
        api = OnlyuserApi('http://127.0.0.1:8000/onlyuser/')        
        ``` 

    '''
    def __init__(self, api_root_url=None, timeout=None):
        super().__init__(
            api_root_url or settings.ONLYUSER_API_URL,
            timeout or settings.API_TIMEOUT 
        )

    def register_resource(self):
        '''注册API资源
        '''
        self._api.add_resource(resource_name='roleperm', resource_class=RolepermResource)

    def query_userids_department(self, app_tag, user_id, organization_id):
        '''查询用户所在部门的全部用户ID列表
           @app_tag           应用标签
           @user_id           用户ID
           @organization_id   当前机构(公司)ID, 在组构机构树中是根节点ID
        '''
        data = {
            'app_tag': app_tag,
            'user_id': user_id,
            'organization_id': organization_id
        }
        return self._request('roleperm', 'userids_department', body=data, headers={'Connection': 'close'})


    def query_userids_branch(self, app_tag, user_id, organization_id):
        '''查询用户所在部门及下属机构的全部用户ID列表
           @app_tag           应用标签
           @user_id           用户ID
           @organization_id   当前机构(公司)ID, 在组构机构树中是根节点ID
        '''
        data = {
            'app_tag': app_tag,
            'user_id': user_id,
            'organization_id': organization_id
        }
        return self._request('roleperm', 'userids_branch', body=data)
    

    def query_userids_organization(self, app_tag, user_id, organization_id, headers={'Connection': 'close'}):
        '''查询用户所在机构(公司)的全部用户ID列表
           @app_tag           应用标签
           @user_id           用户ID
           @organization_id   当前机构(公司)ID, 在组构机构树中是根节点ID
        '''
        data = {
            'app_tag': app_tag,
            'user_id': user_id,
            'organization_id': organization_id
        }
        return self._request('roleperm', 'userids_organization', body=data, headers={'Connection': 'close'})    

#默认接口实例
onlyuserapi = OnlyuserApi()
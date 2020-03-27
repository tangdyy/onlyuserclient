'''onlyuser 客户端中间件
'''

class RoleMiddleware():
    '''角色权限中间件
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        role = None
        if 'X-User-Id' in request.headers:
            role = {}
            role['application_id'] = request.headers.get('X-Application-Id') 
            role['is_admin'] = request.headers.get('X-User-Is-Admin', 'FALSE') == 'TRUE'
            role['user_id'] = request.headers.get('X-User-Id')
            role['username'] = request.headers.get('X-User-Username')
            role['current_org'] = request.headers.get('X-Current-Org', None)
            scopesstr = request.headers.get('X-Roleperm-Scopes')
            if isinstance(scopesstr,str) and len(scopesstr)>0:
                role['scopes'] = scopesstr.split(',')
            else:
                role['scopes'] = []
        request.role = role
        response = self.get_response(request)

        return response 
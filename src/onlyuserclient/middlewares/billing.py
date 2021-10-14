'''计费相关中间件
'''
class BillingMiddleware():
    '''计费控制中间建
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def get_user_id(self, request=None):
        pass


    def __call__(self, request):
        print(dir(self))
        print(dir(request))
        print('this get_response before.')
        response = self.get_response(request)
        print('this get_response after.')
        return response 
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        print(view_func.cls, '\n') 
        print(view_func.actions, '\n')
        print(dir(view_func.cls), '\n')
        print(view_args, view_kwargs, '\n')
        return None
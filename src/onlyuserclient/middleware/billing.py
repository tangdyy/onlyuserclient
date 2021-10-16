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
        response = self.get_response(request)
        return response 
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
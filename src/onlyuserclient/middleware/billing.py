'''计费相关中间件
'''
from rest_framework import status
from rest_framework.response import Response
from onlyuserclient.api import onlyuserapi
from onlyuserclient.settings import billing_settings
from onlyuserclient.settings import onlyuser_settings

class BillingMiddleware():
    '''计费控制中间建
    '''
    def __init__(self, get_response):

        self.get_response = get_response

    def get_user_id(self, request):
        return request.headers.get('X-User-Id', None)

    def get_application_id(self, request):
        return request.headers.get('X-Application-Id', None) 

    def get_current_org_id(self, request):
        return request.headers.get('X-Current-Org', None)



    def __call__(self, request):
        response = self.get_response(request)
        return response 
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        user_id = self.get_user_id(request)
        app_id = self.get_application_id(request)
        org_id = self.get_current_org_id(request)
        app_check = False
        if onlyuser_settings.APPLICATION_SERVICE:
            code, detail = onlyuserapi.apply_application(app_id, user_id, org_id)
            app_check = True
        if not app_check and hasattr(view_func, 'cls'):
            view_application_service = getattr(view_func.cls, 'application_service', False)
            if view_application_service:
                code, detail = onlyuserapi.apply_application(app_id, user_id, org_id)
        setattr(request, '_application_check', app_check)
        if code != 0:
            return Response(
                {
                    'detail': '拒绝服务，请确认你的计费账户已经开通本应用服务项目。'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return None
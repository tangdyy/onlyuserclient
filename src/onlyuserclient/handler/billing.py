from django.utils import timezone
from django.http import HttpRequest
from rest_framework.request import Request

__all__ = (
    'BillApiHandler',
)


class BillApiHandler():
    '''Api计费处理
    '''
    def __init__(
        self,
        service_label, 
        before=True,
        after=True,
        usable=True,
        application_service=False
        ):
        self.service_label = service_label, 
        self.before = before,
        self.after = after,
        self.usable = usable,
        self.application_service = application_service

    def _get_user_id(self, request):
        return request.headers.get('X-User-Id', None)

    def _get_application_id(self, request):
        return request.headers.get('X-Application-Id', None) 

    def _get_current_org_id(self, request):
        return request.headers.get('X-Current-Org', None)

    def _get_request(self, *args, **kwargs):
        if len(args) < 1:
            return None
        if isinstance(args[0], HttpRequest) or isinstance(args[0], Request):
            return args[0]
        if len(args) < 2:
            return None
        if isinstance(args[1], HttpRequest) or isinstance(args[1], Request):
            return args[1]
        return None        

    def get_before_count(self, request=None):
        return 1

    def get_after_count(self, request, response, before_count=1):
        return before_count

    def get_before_start_time(self, request=None):
        return timezone.now()

    def get_after_start_time(self, request, response, before_start_time=None):
        return before_start_time

    def get_finish_time(self):
        return timezone.now()

    def request_service(self, request):
        pass

    def finish_service(self, request, response):
        pass

    def usable_service(self, request):
        pass

    def apply_application(self, request):
        pass

    def before_api(self, *args, **kwargs):
        if not self.before:
            return 
                    
        request = self._get_request(*args, **kwargs)


    def after_api(self, *args, **kwargs):
        request = self._get_request(*args, **kwargs)

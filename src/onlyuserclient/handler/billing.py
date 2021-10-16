from django.utils import timezone

__all__ = (
    'BillApiHandler',
)


class BillApiHandler():
    '''计费处理器
    '''
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
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from onlyuserclient.decorator import api_charge

class Demo1ViewSet(viewsets.ViewSet):
    '''demo1
    '''
    user_bill = True
    organization_bill = False
    
    def list(self, request):
        data = {
            'code': 1,
            'result': 'this is demo1 list.'
        }
        return Response(data)

    @action(
        detail=True, 
        methods=['post'],
        url_name='bill-postpay',
        url_path='bill-postpay'
    )
    @api_charge(
        service='bill1'
    )
    def bill_postpay(self, request, pk=None):
        data = {
            'code': 1,
            'result': 'this is demo1 bill_postpay.'
        }
        return Response(data)

@api_charge(
    service='bill2'
)
def fun_list(request):
    '''函数视图
    '''
    return HttpResponse('aaaaaa')
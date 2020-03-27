from onlyuserclient.viewsets import RoleModelViewSet
from .serializers import DefaultDemoSerializer, CompleteDemoSerializer, HideDemoSerializer
from .models import RoleDemo

class RoleViewSet(RoleModelViewSet):
    queryset = RoleDemo.objects.all()
    user_relate_field = 'owner'
    serializer_classs = {
        'default': DefaultDemoSerializer,
        'complete': CompleteDemoSerializer,
        'part': HideDemoSerializer
    }

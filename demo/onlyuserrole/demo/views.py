from onlyuserclient.viewsets import RoleModelViewSet
from .serializers import DefaultDemoSerializer, CompleteDemoSerializer, HideDemoSerializer
from .models import RoleDemo

class RoleViewSet(RoleModelViewSet):
    queryset = RoleDemo.objects.all()
    user_relate_field = 'owner'
    organization_relate_field = 'organization'
    serializer_classs = {
        'default': DefaultDemoSerializer,
        'complete_view': CompleteDemoSerializer,
        'part_view': HideDemoSerializer
    }

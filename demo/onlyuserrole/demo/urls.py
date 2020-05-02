from django.conf.urls import url
from django.urls import path,include
from rest_framework import  routers

from .views import RoleViewSet

router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    url(r'^', include(router.urls)),  
]

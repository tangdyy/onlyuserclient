from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'demo1s', Demo1ViewSet, basename='demo1')


urlpatterns = [
    url(r'^', include(router.urls)), 
    path('fun-list/', fun_list, name='fun-list'), 
]
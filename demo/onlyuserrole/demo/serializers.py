from rest_framework import serializers
from .models import RoleDemo
from onlyuserclient.serializers import HideCharField


class DefaultDemoSerializer(serializers.ModelSerializer):
    '''此序列化类,部分字段是字读,不能修改
    '''
    class Meta:
        model = RoleDemo
        fields = "__all__"
        read_only_fields = ['name', 'mobile', 'address', 'idcord', 'owner']


class CompleteDemoSerializer(serializers.ModelSerializer):
    '''此序列化类,所有字段都能完全显和修改
    '''
    class Meta:
        model = RoleDemo
        fields = "__all__"


class HideDemoSerializer(serializers.ModelSerializer):
    '''此序列化类,所有字段都能修改,部份字段将部分隐藏
    '''
    mobile = HideCharField( max_length=11, hide_start=3, hide_end=7, fill_char='*')
    address = HideCharField( max_length=11, hide_start=3, hide_end=5, fill_char='*')
    class Meta:
        model = RoleDemo
        fields = "__all__"


class ReadlyMobileDemoSerializer(serializers.ModelSerializer):
    '''此序列化类,所有字段都能完全显和修改
    '''
    class Meta:
        model = RoleDemo
        fields = "__all__"
        read_only_fields=('mobile',)

import datetime
from django.db import models
from django.core.cache import cache
from rest_framework import exceptions,status,viewsets
from onlyuserclient.api import onlyuserapi
from onlyuserclient.settings import api_settings

class RoleModelViewSet(viewsets.ModelViewSet):
    '''角色权限视图集
       使用时必须定义子类,并定义以下属性:
          queryset: Model类的QuerySet实例
          user_relate_field: Model类中保存user_id的字段名
          serializer_classs: 字段权限对应的序列化类,dict结构, key是代表字段权限scope标签, value是序列化类
       以下属性可以选择定义:
          allow_not_auth: 是否允许未认证的用户访问,默认是`False`,如果是`True`,未认证用户访问不受限制
          org_relate_field: Model类中保存organization_id的字段名

       用scope标签标记角色的记录权限范围,默认实现了按组织机构定义的scope如下：
           'all':          可以操作全部记录
           'owner':        可以操作自已拥有的记录
           'department':   可以操作本部门的的记录
           'branch':       可以操作本部门及下属单位的记录
           'organization': 可以操作所在组织的记录
    '''
    
    DEFAULT_SCOPE_LEVEL={
        'owner': 1,        
        'department': 2,
        'branch': 3,       
        'organization': 4, 
        'all': 5, 
    }

    def get_queryset(self):
        qset = getattr(self, 'queryset')
        if qset is None: 
            raise AttributeError("Attribute 'queryset' must be defined.")
        if not isinstance(qset, models.QuerySet):
            raise AttributeError("Attribute 'queryset' must be an instance of 'QuerySet'.")
        allow_not_auth = getattr(self, 'allow_not_auth', True)

        role = getattr(self.request, 'role', None)
        if allow_not_auth and role is None: 
            return qset

        if not allow_not_auth and role is None: 
            return qset.none()

        relate_field = getattr(self,'user_relate_field')
        if relate_field is None:
            raise AttributeError("Attribute 'user_relate_field' must be defined.")

        scopes = role.get('scopes',[])
        
        is_admin = role.get('is_admin')
        if is_admin:
            return qset

        application_id = role.get('application_id', None)
        user_id = role.get('user_id', None)
        organization_id = role.get('current_org', None)
        ids = self.get_ids_from_scopes(scopes, application_id, user_id, organization_id)

        if ids == 'all':
            return qset
        else:
            if ids is None:
                ids =[]
            org_relate_field = getattr(self,'org_relate_field', None)
            if org_relate_field:
                codestr = "qset.filter(%s=organization_id, %s__in=ids)"%(org_relate_field, relate_field,) 
            else:
                codestr = "qset.filter(%s__in=ids)"%(relate_field,)
            qset=eval(codestr, globals(), locals())            
        return qset


    def get_ids_from_scopes(self, scopes=[], application_id=None, user_id=None, organization_id=None):
        '''根据范围标签列表返加用户ID列表
           默认实现all,owner,department, branch, organization五个标签 
           可以在子类中重载此方法,定义自已的标签和记录权限控制规则
        '''
        #取最大范围
        max_scope = None
        max_scope_level = 0
        for v in scopes:
            level = self.DEFAULT_SCOPE_LEVEL.get(v, 0)
            if level > max_scope_level:
                max_scope = v
                max_scope_level = level

        if  max_scope == 'all':
            return 'all'

        if max_scope == 'owner':
            return [user_id,]

        ids = None
        cache_key = application_id + user_id + organization_id + max_scope
        if api_settings.CACHE_API:
            ids = cache.get(cache_key)

        if ids:
            return ids

        data = {
        	"app_id":application_id,
        	"user_id":user_id,
        	"organization_id":organization_id
        }
        res = None
        try:
            if max_scope == 'organization':
                res = onlyuserapi.roleperms.userids_organization(body=data)
            elif max_scope == 'branch':
                res = onlyuserapi.roleperms.userids_branch(body=data)
            elif max_scope == 'department':
                res = onlyuserapi.roleperms.userids_department(body=data)
        except:
            pass

        ids = []
        if res and res.status_code==200:
            if isinstance(res.body,list):
                ids=res.body
                if api_settings.CACHE_API:
                    cache.set(cache_key, ids, api_settings.CACHE_TTL)
   
        return ids

    def get_serializer_class(self):
        '''根据字段权限标签切换序列化类
        '''
        serializer_classs = getattr(self, 'serializer_classs', None)
        if serializer_classs is None:
            raise AttributeError("Attribute 'serializer_classs' must be defined.")
        serializer_class = None
        role = getattr(self.request, 'role', None)
        if role and 'scopes' in role:
            scopes = role['scopes']
            for scope in scopes:
                if scope in serializer_classs:
                    serializer_class = serializer_classs[scope]
                    break
        if serializer_class is None:
            serializer_class = serializer_classs.get('default')
        return serializer_class

    def create(self, request):
        if hasattr(self, 'creater'):  
            creater = request.role.get('user_id', '0') if hasattr(request, 'role') else '0'
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            if self.creater == True:
                request.data['creater'] = creater
                request.data['create_time'] = create_time
            elif isinstance(self.creater, tuple) or isinstance(self.creater, list):
                if len(self.creater) > 0 and isinstance(self.creater[0], str):
                    request.data[self.creater[0]] = creater
                if len(self.creater) > 1 and isinstance(self.creater[1], str):
                    request.data[self.creater[1]] = create_time               
        return super().create(request)       

    def partial_update(self, request, pk=None):
        return super().partial_update(request, pk)
    
    def update(self, request, pk=None):
        return super().update(request, pk)
     
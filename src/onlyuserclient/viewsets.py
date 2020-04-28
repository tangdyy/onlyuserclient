from django.db import models
from rest_framework import exceptions,status,viewsets
from onlyuserclient.apis.onlyuser import onlyuserapi


class RoleModelViewSet(viewsets.ModelViewSet):
    '''角色权限视图集
       使用时必须定义子类,并定义以下属性:
          queryset: Model类的QuerySet实例
          user_relate_field: Model类中保存user_id的字段名
          organization_relate_field: Model类中保存organization_id的字段名
          serializer_classs: 字段权限对应的序列化类,dict结构, key是代表字段权限scope标签, value是序列化类
       以下属性可以选择定义:
          allow_not_auth: 是否允许未认证的用户访问,默认是`False`,如果是`True`,未认证用户访问不受限制

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
        relate_field = getattr(self,'user_relate_field')
        if relate_field is None:
            raise AttributeError("Attribute 'user_relate_field' must be defined.")

        allow_not_auth = getattr(self, 'allow_not_auth', False)
        role = getattr(self.request, 'role', None)
        scopes = None
        if allow_not_auth and role :
            scopes = role.get('scopes', None)
        elif role is None or not 'scopes' in role:
            raise exceptions.NotAuthenticated()
        else:
            scopes = role['scopes']
        
        if allow_not_auth and scopes is None:
            return qset
        
        is_admin = role.get('is_admin')
        if is_admin:
            return qset
        application_id = role.get('application_id')
        user_id = role.get('user_id')
        organization_id = role.get('current_org')
        ids = self.get_ids_from_scopes(scopes, application_id, user_id, organization_id)

        if ids == 'all':
            return qset
        else:
            if ids is None:
                ids =[]
            org_relate_field = getattr('organization_relate_field', None)
            if org_relate_field:
                codestr = "qset.filter(%s=organization_id, %s__in=ids)"%(org_relate_field,relate_field,) 
            else:
                codestr = "qset.filter(%s__in=ids)"%(relate_field,)
            qset=eval(codestr,globals(),locals())            
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

        if max_scope == 'all':
            return 'all'
        elif max_scope == 'organization':
            return onlyuserapi.query_userids_organization(application_id, user_id, organization_id)
        elif max_scope == 'branch':
            return onlyuserapi.query_userids_branch(application_id, user_id, organization_id)
        elif max_scope == 'department':
             return onlyuserapi.query_userids_department(application_id, user_id, organization_id)
        elif max_scope == 'owner':
            return [user_id]
        return []

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

        
from collections.abc import Iterable
from rest_framework.serializers import ListSerializer


__all__ = [
    'ApiRelatedListSerializer'
]


class ApiRelatedListSerializer(ListSerializer):
    """Api related list serializer

    Cooperate with 'ApiRelatedField' to reduce API access times.
    """
    def to_representation(self, data):
        datas = super().to_representation(data)
        for name, field in self.child._declared_fields.items():
            if field.__class__.__name__ == 'ApiRelatedField':
                ids = {}
                for index, item in enumerate(datas):
                    if item[name] not in ids:                        
                        ids[item[name]] = [index]
                    else:
                        ids[item[name]].append(index)

                objs = field._get_related_objects(ids.keys())
                if isinstance(objs, Iterable) and not isinstance(objs, str):
                    for obj in objs:
                        for index in ids[obj['id']]:                  
                            datas[index][name] = obj
        return datas


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
                ids = { item[name]: index for index, item in enumerate(datas) }
                objs = field._get_related_objects(ids.keys())
                
                for obj in objs:
                    datas[ids[obj['id']]][name] = obj           
        return datas


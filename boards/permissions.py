from rest_framework.permissions import *


class IsPoster(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS', ]:
            return True
        else:
            return request.user.id == obj.poster_id

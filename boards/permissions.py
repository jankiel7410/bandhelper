from rest_framework.permissions import *


class IsPosterOrAdmin(BasePermission):
    def has_object_permission(self, request, view, song):
        if request.method in ['GET', 'OPTIONS', ]:
            return True
        else:
            is_poster = request.user.id == song.poster_id
            if is_poster:
                return True
            is_admin = request.user.id == song.list.board.admin_id
            return is_admin


class IsAdmin(BasePermission):

    def has_object_permission(self, request, view, song):
        if request.method in ['GET', 'OPTIONS', ]:
            return True

        return request.user.id == song.list.board.admin_id


class CanInvite(BasePermission):

    def has_object_permission(self, request, view, membership):
        if request.method in ['GET', 'OPTIONS', ]:
            return True

        return request.user.id == membership.board.admin_id

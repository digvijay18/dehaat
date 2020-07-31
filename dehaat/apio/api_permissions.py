from rest_framework import permissions

from dehaat.settings import ADMIN_GROUP


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.user.groups.first().name == ADMIN_GROUP:
            return True
        return False

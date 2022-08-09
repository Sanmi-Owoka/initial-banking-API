from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return user.is_admin
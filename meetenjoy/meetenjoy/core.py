from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsLector(BasePermission):
    def has_permission(self, request, view):
        return request.user.get_lector() is not None


class IsVisitor(BasePermission):
    def has_permission(self, request, view):
        return request.user.get_visitor() is not None

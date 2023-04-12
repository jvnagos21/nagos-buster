from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Movie


class IsAdmOrReadOnly(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        return (
            req.method in permissions.SAFE_METHODS
            or req.user.is_authenticated
            and req.user.is_staff
        )

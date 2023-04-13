from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsAccountEmployeeOrNot(permissions.BasePermission):
    def has_object_permission(self, req: Request, view, obj=User) -> bool:
        return req.user == obj or req.user.is_authenticated and req.user.is_staff

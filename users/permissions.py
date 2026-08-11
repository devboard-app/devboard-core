from django.conf import settings
from rest_framework.permissions import BasePermission


class IsInternalService(BasePermission):
    def has_permission(self, request, view):
        key = request.headers.get('X-Service-Key')
        return key == settings.INTERNAL_API_KEY

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"
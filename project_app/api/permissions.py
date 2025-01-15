from rest_framework import permissions

#make only the user who have the token can access it or edit it
class AuthUserPermission(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.user == request.user
from rest_framework import permissions


class ModeratorsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            return False

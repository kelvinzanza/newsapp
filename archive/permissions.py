from rest_framework import permissions


class IsContentOwnerOrEditor(permissions.BasePermission):
    '''
    Custom permission to only allow editors to edit any content and
    journalists to edit their own content.
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name='Editor').exists():
            return True

        if (request.user.groups.filter(name='Journalist').exists() and
                view.action == 'create'):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name='Editor').exists():
            return True

        return obj.author == request.user

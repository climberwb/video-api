from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsMember(permissions.BasePermission):
    """
    Checkes if the user is a member of the service
    """
    
    def has_permission(self, request,view):
        free_preview = view.get_object().free_preview

        if request.user.is_authenticated() or free_preview:
            try:
                is_member = request.user.is_member
            except:
                is_member = None
            if is_member or free_preview:
                return True
            else:
                raise PermissionDenied("You must be a member to view this.")
        raise PermissionDenied("You must be logged in to view this.")
                
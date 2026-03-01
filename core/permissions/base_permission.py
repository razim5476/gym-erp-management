"""
Docstring for core.permissions.base_permission
"""


from rest_framework.permissions import BasePermission
from guardian.shortcuts import get_objects_for_user


class GuardianPermission(BasePermission):
    """
    Generic Guardian permission for DRF ViewSets
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Superuser bypass
        if user.is_superuser:
            return True

        action = view.action

        permission_map = getattr(view, "permission_map", None)
        if not permission_map:
            return True  # allow if not defined

        perm = permission_map.get(action)
        if not perm:
            return True

        # CREATE is global permission
        if action == "create":
            return user.has_perm(perm)

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        action = view.action
        permission_map = getattr(view, "permission_map", None)
        if not permission_map:
            return True

        perm = permission_map.get(action)
        if not perm:
            return True

        return user.has_perm(perm, obj)

"""
User services.
"""


class UserServices:
    """User related services and methods."""

    @staticmethod
    def has_permission(self, request, view):
        """check for role and has the permissions."""
        
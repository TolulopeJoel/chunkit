from rest_framework.permissions import DjangoModelPermissions


class IsSuperUser(DjangoModelPermissions):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

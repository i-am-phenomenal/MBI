from rest_framework.permissions import IsAuthenticated

class ModelMixin:
    """
    Mixin class to setup the look_up field to id in retreive and delete views
    """
    lookup_field = "id"

class PermissionMixin:
    """
    Mixin class to set the permission_classes to IsAuthenticated
    """
    permission_classes = [IsAuthenticated]   
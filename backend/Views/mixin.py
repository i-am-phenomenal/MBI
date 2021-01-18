
class ModelMixin:
    """
    Mixin class to setup the look_up field to id in retreive and delete views
    """
    lookup_field = "id"
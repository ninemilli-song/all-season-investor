from ..models import AssetType
from ..serializer import AssetTypeSerializer
from rest_framework import mixins, viewsets, permissions


class FundView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    POST auth/login/
    资产标的 视图
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    # Override global authentication class in there
    # Then there have no authentication class with the statement below.
    authentication_classes = ()

    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer

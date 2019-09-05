from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import InvestRecord
from ..serializer import InvestRecordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from rest_framework import exceptions


class InvestRecordView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    投资记录视图
    """

    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    # Override global authentication class in there
    # Then there have no authentication class with the statement below.
    authentication_classes = ()

    queryset = InvestRecord.objects.all()
    serializer_class = InvestRecordSerializer

    def create(self, request, *args, **kwargs):
        # Create the instance of JSONWebTokenAuthentication to do the authentication job
        authentication = JSONWebTokenAuthentication()

        # try:
        '''
        authentication.authenticate 会抛出异常，所以添加异常捕获
        '''
        auth_data = authentication.authenticate(request)
        if auth_data is None:
            raise exceptions.NotAuthenticated()

        owner = auth_data[0].investor

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=owner)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
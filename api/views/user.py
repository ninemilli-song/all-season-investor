from django.contrib.auth import login, authenticate, user_logged_in
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from ..models import Investor, Sex
from ..serializer import InvestorSerializer, \
    JWTSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, APIView
from datetime import datetime
from rest_framework import exceptions
from ..forms import SignUpForm

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginView(ObtainJSONWebToken):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    # Override global authentication class in there
    # Then there have no authentication class with the statement below.
    authentication_classes = ()

    serializer_class = JWTSerializer

    # Override the post method of the super class
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            # response_data = jwt_response_payload_handler(token, user, request)

            # Get investor information by user
            # Then add investor information into response
            investor = Investor.objects.get(user=user)
            investor_data = InvestorSerializer(investor)
            response = Response({
                'token': token,
                'user': investor_data.data
            })

            # Set JWT Token into Cookie
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.now() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(VerifyJSONWebToken):

    serializer_class = InvestorSerializer

    def get(self, request, format=None):

        # Create the instance of JSONWebTokenAuthentication to do the authentication job
        authentication = JSONWebTokenAuthentication()

        # try:
        '''
        authentication.authenticate 会抛出异常，所以添加异常捕获
        '''
        auth_data = authentication.authenticate(request)
        if auth_data is None:
            raise exceptions.NotAuthenticated()

        '''
        auth_data type is tuple, first is user instance, the second is jwt value.
        So I serializer the investor attribute of the first argument.
        '''
        serializer = self.get_serializer(auth_data[0].investor)

        '''
        Response the data
        '''
        return Response(serializer.data)

        # except BaseException as exc:
        #     return Response(exc, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
def signup(request):
    """
    注册视图
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = SignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.investor.mobile = form.cleaned_data.get('mobile')
            sex = Sex.objects.get(id=form.cleaned_data.get('sex') or 1)
            user.investor.sex = sex
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            payload = jwt_payload_handler(user)
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            investor = Investor.objects.get(user=user)
            investor_data = InvestorSerializer(investor)
            return Response({
                'token': jwt_encode_handler(payload),
                'user': investor_data.data
            })

        return Response({'message': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_404_NOT_FOUND)


class Profile(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    所有用户资产列表
    """
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = InvestorSerializer

    def get_queryset(self):
        return Investor.objects.all()

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        user_assets = []

        for user in users:
            user_asset = self.get_serializer(user).data
            total_amount = 0
            assets = user.asset_set.all()
            for asset in assets:
                total_amount += asset.pv
            user_asset['amount'] = total_amount
            user_assets.append(user_asset)

        return Response(user_assets)

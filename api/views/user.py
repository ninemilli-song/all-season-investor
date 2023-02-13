from django.contrib.auth import login, authenticate, user_logged_in
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from ..models import Investor, Sex
from ..serializer import InvestorSerializer, \
    LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..forms import SignUpForm

# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# @api_view(['GET', 'POST'])
class LoginView(generics.GenericAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    # # Override global authentication class in there
    # # Then there have no authentication class with the statement below.
    # authentication_classes = ()
    #
    serializer_class = LoginSerializer

    # Override the post method of the super class
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        investor_obj = Investor.objects.get(user=user)
        investor_data = InvestorSerializer(investor_obj).data

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': investor_data,
            'token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)


class UserInfo(generics.RetrieveAPIView):

    serializer_class = InvestorSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Investor.objects.all()

    def get_object(self):
        investors = self.get_queryset()
        for investor in investors:
            if self.request.user.id == investor.user.id:
                return investor
    # def get(self, requst):
    #     investors = self.get_object()
    #     serializer = self.get_serializer(investors)
    #     return Response(serializer.data)


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
            # payload = jwt_payload_handler(user)
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            investor = Investor.objects.get(user=user)
            investor_data = InvestorSerializer(investor)
            return Response({
                # 'token': jwt_encode_handler(payload),
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

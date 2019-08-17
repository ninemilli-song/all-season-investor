from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, user_logged_in
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Investor, Asset, Bucket, Sex, Initial
from .serializer import AssetSerializer, InvestorSerializer, JWTSerializer, BucketSerializer, UserSerializer, InitialSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken
from datetime import datetime
from rest_framework import exceptions
from .forms import SignUpForm

# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def index(request):
    users = Investor.objects.all()

    # 用户资产列表
    user_assets = []

    for user in users:
        user_asset = {
            "user": user
        }
        total_amount = 0
        assets = user.asset_set.all()
        for asset in assets:
            total_amount += asset.amount
        user_asset['amount'] = total_amount
        user_assets.append(user_asset)

    context = {
        'user_assets': user_assets
    }

    return render(request, 'api/index.html', context)


# 用户资产详情
def assetView(request, user_id):
    user = get_object_or_404(Investor, pk=user_id)
    assets = user.asset_set.all()

    return render(request, 'api/asset_detail.html', {
        "user": user,
        "assets": assets
    })


class Profile(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    用户资产列表
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
                total_amount += asset.amount
            user_asset['amount'] = total_amount
            user_assets.append(user_asset)

        return Response(user_assets)


class InvestorAssets(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = AssetSerializer

    # permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Asset.objects.all()

    @action(detail=False, url_name='get_assets_by_user', url_path='user')
    def get_assets_by_user(self, request, *args, **kwargs):
        """
        根据用户id查看用户资产
        """
        user_id = request.query_params['id']
        user = get_object_or_404(Investor, pk=user_id)
        queryset = user.asset_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_name='get_analysis_by_user', url_path='analysis')
    def get_analysis_by_user(self, request, *args, **kwargs):
        """Get all asset of the user"""
        user_id = request.query_params['id']
        user = get_object_or_404(Investor, pk=user_id)
        assets_queryset = user.asset_set.all()
        assets_serializer = self.get_serializer(assets_queryset, many=True)

        buckets_queryset = Bucket.objects.all()
        buckets_serializer = BucketSerializer(buckets_queryset, many=True)

        analysis_list = []
        for bucket in buckets_serializer.data:
            analysis_item = {
                'bucket': bucket,
                'assets': [],
                'amount': 0,
                'suggestAmount': 0,
                'rate': 0.5,
                'suggestRate': 0.2,
                'title': '',
                'analysis': ''
            }

            # 所有资产总额
            total_amount = 0
            for asset in assets_serializer.data:
                total_amount += asset['amount']

                # 资产和金额归类
                if asset['type']['category']['level']['code'] == bucket['code']:
                    analysis_item['assets'].append(asset)
                    analysis_item['amount'] += asset['amount']

            analysis_item['suggestRate'] = bucket['rate']
            analysis_item['suggestAmount'] = round(total_amount * analysis_item['suggestRate'], 2)
            analysis_item['rate'] = round(analysis_item['amount'] / total_amount, 3)
            analysis_item['title'] = bucket['description']

            tip = ''
            if (analysis_item['rate'] - analysis_item['suggestRate']) > 0.1:
                if (bucket['code'] == '000001') : tip = '过于保守，可能会拉低收益'
                if (bucket['code'] == '000002') : tip = '过于激进，风险过高'
                analysis_item['analysis'] = '配置比例过高，%s！' % (tip,)
            elif (analysis_item['rate'] - analysis_item['suggestRate'] < 0.1):
                if (bucket['code'] == '000001') : tip = '过于保守，可能会拉低收益'
                if (bucket['code'] == '000002') : tip = '过于激进，风险过高'
                analysis_item['analysis'] = '配置比例过低，%s！' % (tip,)
            else:
                analysis_item['analysis'] = '资产配置健康！'

            analysis_list.append(analysis_item)

        return Response(analysis_list)


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


class InitialView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    期初数据 视图
    """
    queryset = Initial.objects.all()
    serializer_class = InitialSerializer

    def create(self, request, *args, **kwargs):
        """
        创建期初数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # TODO: 通过基金id查询基金
        # TODO: 保存基金、起始时间、起始金额数据
        pass

    def update(self, request, *args, **kwargs):
        """
        更新期初数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # TODO: 通过基金id查询基金
        # TODO: 保存基金、起始时间、起始金额数据

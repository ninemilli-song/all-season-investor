from django.shortcuts import render, get_object_or_404
from .models import Investor, Asset
from .serializer import AssetSerializer, InvestorSerializer, TokenSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
import json
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from datetime import datetime

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


'''
用户资产列表
'''


class Investors(viewsets.ViewSet):

    def list(self, request):
        users = Investor.objects.all()

        user_assets = []

        for user in users:
            user_asset = InvestorSerializer(user).data
            total_amount = 0
            assets = user.asset_set.all()
            for asset in assets:
                total_amount += asset.amount
            user_asset['amount'] = total_amount
            user_assets.append(user_asset)

        return Response(user_assets)


'''
根据用户id查看用户资产
'''


class InvestorAssets(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = AssetSerializer

    def get_queryset(self):
        return Asset.objects.all()

    """根据用户id查询资产"""

    @action(detail=False, url_name='get_assets_by_user', url_path='user')
    def get_assets_by_user(self, request, *args, **kwargs):
        user_id = request.query_params['id']
        user = get_object_or_404(Investor, pk=user_id)
        queryset = user.asset_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """异常处理"""
    def handle_exception(self, exc):
        if (type(exc) == MultiValueDictKeyError):
            return Response({
                'msg': '参数不合法'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'msg': '其它错误'
        }, status=status.HTTP_400_BAD_REQUEST)


"""
登陆视图
"""


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
            response = Response(investor_data.data)

            # Set JWT Token into Cookie
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
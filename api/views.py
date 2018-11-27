from django.shortcuts import render, get_object_or_404
from .models import User, Asset
from .serializer import AssetSerializer, UserSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
import json
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.


def index(request):
    users = User.objects.all()

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
    user = get_object_or_404(User, pk=user_id)
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
        users = User.objects.all()

        user_assets = []

        for user in users:
            user_asset = UserSerializer(user).data
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
        user = get_object_or_404(User, pk=user_id)
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
            })

        return Response({
            'msg': '其它错误'
        }, status=404)

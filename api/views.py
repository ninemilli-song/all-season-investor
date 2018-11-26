from django.shortcuts import render, get_object_or_404
from .models import User, Asset
from .serializer import AssetSerializer, UserSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
import json
from rest_framework import mixins

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
class UserList(APIView):

    def get(self, request):
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
class UserDetail(generics.ListAPIView):

    serializer_class = AssetSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_id)
        return user.asset_set.all()

    def handle_exception(self, exc):
        return Response({
            'msg': '用户未找到'
        }, status=404)


"""更新资产"""
class UpdateAssetAmount(RetrieveUpdateAPIView):

    serializer_class = AssetSerializer

    def get_object(self):
        user_id = self.kwargs['user']
        user = get_object_or_404(User, pk=user_id)
        asset_id = self.kwargs['asset']
        asset = user.asset_set.get(id=asset_id)
        return asset

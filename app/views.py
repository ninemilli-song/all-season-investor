from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
from rest_framework.exceptions import APIException

from .models import User, Asset
from .serializer import AssetSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import json

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

    return render(request, 'app/index.html', context)


# 用户资产详情
def asset(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    assets = user.asset_set.all()

    return render(request, 'app/asset_detail.html', {
        "user": user,
        "assets": assets
    })


class AssetView(APIView):

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        assets = user.asset_set.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def handle_exception(self, exc):
        return Response({
            'msg': '用户未找到'
        }, status=404)

from django.shortcuts import render, get_object_or_404
from ..models import Investor, Asset, Bucket
from ..serializer import AssetSerializer, BucketSerializer
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions


class InvestorAssets(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        return Asset.objects.all()

    @action(detail=False, url_name='get_assets_by_user', url_path='user')
    def get_assets_by_user(self, request, *args, **kwargs):
        """
        根据用户id查看用户资产
        """
        # Create the instance of JSONWebTokenAuthentication to do the authentication job
        authentication = JSONWebTokenAuthentication()

        # try:
        '''
        authentication.authenticate 会抛出异常，所以添加异常捕获
        '''
        auth_data = authentication.authenticate(request)
        if auth_data is None:
            raise exceptions.NotAuthenticated()

        user = auth_data[0].investor

        # user_id = request.query_params['id']
        # user = get_object_or_404(Investor, pk=user_id)
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
        # Create the instance of JSONWebTokenAuthentication to do the authentication job
        authentication = JSONWebTokenAuthentication()

        # try:
        '''
        authentication.authenticate 会抛出异常，所以添加异常捕获
        '''
        auth_data = authentication.authenticate(request)
        if auth_data is None:
            raise exceptions.NotAuthenticated()

        user = auth_data[0].investor

        # user_id = request.query_params['id']
        # user = get_object_or_404(Investor, pk=user_id)
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
                total_amount += asset['pv']

                # 资产和金额归类
                if asset['type']['category']['level']['code'] == bucket['code']:
                    analysis_item['assets'].append(asset)
                    analysis_item['amount'] += asset['pv']

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
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import Asset, Initial
from ..serializer import AssetSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.views import APIView
from datetime import datetime
from rest_framework import exceptions


class FundListView(APIView):
    """
    Get fund list
    *
    """
    def get(self, request, format=None):
        """
        Return a list of fund
        :param request:
        :param format:
        :return:
        """
        # Create the instance of JSONWebTokenAuthentication to do the authentication job
        authentication = JSONWebTokenAuthentication()
        auth_data = authentication.authenticate(request)
        if auth_data is None:
            raise exceptions.NotAuthenticated()

        owner = auth_data[0].investor

        result = []
        # 获取当前用户的定投期初数据
        initials = Initial.objects.filter(owner=owner.id)

        for initial in initials:
            # 根据基金id & 用户 获取基金档案数据
            try:
                fund = Asset.objects.get(type=initial.fund.id, owner=owner.id)
                # 现值 - 成本 = 收率
                principal = fund.principal
                if principal == 0:
                    principal = initial.start_amount
                profit = fund.pv - principal
                # 利润 / 成本 = 收益率
                profit_rate = profit / principal
                # 投资时长（秒） = 当前时间（秒） - 定投开始时间（秒）
                delta_time = datetime.now().timestamp() - initial.start_time.timestamp()
                # 投资天数 = 投资时长（秒）/ (24 * 60 * 60)
                delta_days = delta_time / (24 * 60 * 60)
                # 年化收益 = 收益率 / (投资天数 / 365)
                profit_rate_annual = profit_rate / (delta_days / 365)

                result.append({
                    'fund': AssetSerializer(fund).data,
                    'principal': fund.principal,
                    'pv': fund.pv,
                    'profit': profit,
                    'profitRate': profit_rate,
                    'profitRateAnnual': profit_rate_annual
                })
            except Asset.DoesNotExist:
                pass

        return Response(result, status=status.HTTP_200_OK)
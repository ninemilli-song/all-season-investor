from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import Initial, InvestRecord, AssetType, Dividend
from ..serializer import AssetTypeSerializer
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
                asset_type = AssetType.objects.get(id=initial.fund.id)
                # 本金 = 定投期初金额 + 定投累积金额
                invest_records = InvestRecord.objects.filter(fund=initial.fund.id, owner=owner.id)
                # 计算成本
                pv = 0
                cur_data_time = None
                acc_amount = 0
                for invest_record in invest_records:
                    acc_amount += invest_record.amount
                    # 查找当前市值，以定投记录中时间最近的市值为准
                    if cur_data_time is None or cur_data_time < invest_record.date_time:
                        cur_data_time = invest_record.date_time
                        pv = invest_record.pv

                principal = float('%.2f' % (initial.start_amount + acc_amount))

                # 统计历史分红总计
                dividends = Dividend.objects.filter(fund=initial.fund.id)
                dividend_amount = 0
                for dividend in dividends:
                    dividend_amount += dividend.amount

                # 收益 = （现值 + 历史分红） - 成本
                profit = float('%.2f' % (pv + dividend_amount - principal))

                # 收益率 = 利润 / 成本
                profit_rate = float('%.4f' % (profit / principal))

                # 投资时长（秒） = 当前时间（秒） - 定投开始时间（秒）
                delta_time = datetime.now().timestamp() - initial.start_time.timestamp()

                # 投资天数 = 投资时长（秒）/ (24 * 60 * 60)
                delta_days = int(delta_time / (24 * 60 * 60))
                print('👉🏻 ---> delta_days is: ', delta_days)

                # 年化收益 = 收益率 / (投资天数 / 365)
                profit_rate_annual = float('%.4f' % (profit_rate / (delta_days / 365)))

                result.append({
                    'assetType': AssetTypeSerializer(asset_type).data,  # 基金
                    'principal': principal,                             # 本金
                    'pv': pv,                                           # 市值
                    'profit': profit,                                   # 收益
                    'profitRate': profit_rate,                          # 收益率
                    'profitRateAnnual': profit_rate_annual,             # 年化收益率
                    'startTime': initial.start_time.timestamp(),        # 起始时间
                    'startAmount': initial.start_amount                 # 起始金额
                })
            except AssetType.DoesNotExist:
                pass

        return Response(result, status=status.HTTP_200_OK)

"""
投资记录视图
每一条定投明细
"""
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import InvestRecord, Initial
from ..serializer import InvestRecordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from rest_framework import exceptions


class InvestRecordView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    # Override global authentication class in there
    # Then there have no authentication class with the statement below.
    authentication_classes = ()

    queryset = InvestRecord.objects.all()
    serializer_class = InvestRecordSerializer

    def create(self, request, *args, **kwargs):
        # Create the instance of JSONWebTokenAuthentication to do the authentication job
        authentication = JSONWebTokenAuthentication()

        # try:
        '''
        authentication.authenticate 会抛出异常，所以添加异常捕获
        '''
        auth_data = authentication.authenticate(request)
        if auth_data is None:
            raise exceptions.NotAuthenticated()

        owner = auth_data[0].investor

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=owner)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        fund_id = request.query_params.get('fund')
        invest_record_queryset = self.get_queryset()
        if fund_id is not None:
            invest_record_queryset_fund_id = invest_record_queryset.filter(fund=fund_id)
            queryset = self.filter_queryset(invest_record_queryset_fund_id).order_by('-date_time')
        else:
            queryset = self.filter_queryset(invest_record_queryset).order_by('-date_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # 本基金的期初数据
        fund_initial = Initial.objects.get(fund=fund_id)
        fund_initial_start_amount = fund_initial.start_amount
        fund_initial_start_time = fund_initial.start_time

        for item in serializer.data:
            # 计算到当前定投记录时间为止的定投成本
            cur_principal = fund_initial_start_amount
            for i in serializer.data:
                # 将定投时间下于当前定投记录时间的投入金额记入成本中
                if float(item.get('date_time')) >= float(i.get('date_time')):
                    cur_principal += i.get('amount')
            # 计算当前定投记录时间点下的收益 profit
            cur_profit = float('%.2f' % (item.get('pv') - cur_principal))
            # 计算当前定投记录时间眯下的收益率 profit_rate
            cur_profit_rate = float('%.4f' % (cur_profit / cur_principal))
            # 计算当前定投记录时间点下的年化收益率 profit_rate_annual
            delta_time = float(item.get('date_time')) - fund_initial_start_time.timestamp()
            delta_days = int(delta_time / (24 * 60 * 60))
            # 年化收益 = 收益率 / (投资天数 / 365)
            profit_rate_annual = float('%.4f' % (cur_profit_rate / (delta_days / 365)))

            # 补充数据
            item['cur_profit'] = cur_profit
            item['cur_profit_rate'] = cur_profit_rate
            item['profit_rate_annual'] = profit_rate_annual

        return Response(serializer.data)

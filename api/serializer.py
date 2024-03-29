from rest_framework import serializers
from .models import Asset, AssetType, AssetCategory, Bucket, Sex, Investor, Initial, InvestRecord
from django.contrib.auth.models import User
# from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, user_logged_in
from datetime import datetime, timezone, timedelta


class BucketSerializer(serializers.ModelSerializer):
    # 自定义name attribute
    description = serializers.SerializerMethodField('get_customize_description')

    def get_customize_description(self, bucket):
        return bucket.description if bucket.description != None else ''

    class Meta:
        model = Bucket
        fields = '__all__'


class AssetCategorySerializer(serializers.ModelSerializer):
    level = BucketSerializer()

    class Meta:
        model = AssetCategory
        fields = ('name', 'code', 'level')


class AssetTypeSerializer(serializers.ModelSerializer):
    category = AssetCategorySerializer()

    class Meta:
        model = AssetType
        fields = ('id', 'name', 'code', 'category')


class SexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sex
        fields = ('label', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class InvestorSerializer(serializers.ModelSerializer):
    sex = serializers.SlugRelatedField(
        read_only=True,
        slug_field='label'
    )

    user = UserSerializer()

    # 自定义name attribute
    name = serializers.SerializerMethodField('get_sysusr_username')

    def get_sysusr_username(self, investor):
        return investor.user.username

    # 自定义 email attribute
    email = serializers.SerializerMethodField('get_sysusr_email')

    def get_sysusr_email(self, investor):
        return investor.user.email

    class Meta:
        model = Investor
        fields = ('id', 'sex', 'name', 'email', 'mobile', 'user')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: return a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        investor, created = Investor.objects.update_or_create(
            user=user,
            mobile=validated_data.pop('mobile')
        )
        return investor


class AssetSerializer(serializers.ModelSerializer):
    owner = InvestorSerializer(read_only=True)
    type = AssetTypeSerializer(read_only=True)

    class Meta:
        model = Asset
        fields = ('id', 'type', 'owner', 'pv')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user and user.is_active:
            return user

        raise serializers.ValidationError('Incorrect credentials')
        # credential = {
        #     self.username_field: attrs.get(self.username_field),
        #     'password': attrs.get('password')
        # }
        #
        # if all(credential.values()):
        #     user = authenticate(request=self.context['request'], **credential)
        #
        #     if user:
        #         if not user.is_active:
        #             msg = 'User account is disabled.'
        #             raise serializers.ValidationError(msg)
        #
        #         payload = jwt_payload_handler(user)
        #         user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
        #
        #         return {
        #             'token': jwt_encode_handler(payload),
        #             'user': user
        #         }
        #     else:
        #         msg = 'Unable to log in with provided credentials.'
        #         raise serializers.ValidationError(msg)
        # else:
        #     msg = 'Must include "{username_field}" and "password".'
        #     msg = msg.format(username_field=self.username_field)
        #     raise serializers.ValidationError(msg)


class InitialSerializer(serializers.ModelSerializer):
    """
    期初数据序列化

    """

    # 基金模型不可编辑
    # 前端传入基金id 后台通过id查询基金模型 进行数据的创建及更新
    fund = AssetTypeSerializer(read_only=True)
    start_time = serializers.DateTimeField(format="%s.%f")

    def validate_fund(self, value):
        """
        自定义 fund 字段的校验
        id 只判断类型 & 数据是否存在
        """
        if type(value) == 'int':
            raise serializers.ValidationError("Field fund type is not int.")

        try:
            fund = AssetType.objects.get(pk=value)
        except AssetType.DoesNotExist:
            raise serializers.ValidationError(f'Fund {value} dose not exist.')

        return value

    def to_internal_value(self, data):
        """
        修改反序列化行为
        由于fund参数为id 需要将其转换成对应的fund数据 所以使用此方法进行转换
        """
        if 'fund' in data:
            fund_id = data.pop('fund', None)
            try:
                fund = AssetType.objects.get(pk=fund_id)
            except AssetType.DoesNotExist:
                raise serializers.ValidationError(f'Fund {fund_id} dose not exist.')

            data['fund'] = fund

        # 转换start_time
        # 前端传入timestamps为毫秒级 需要转换成python的秒级timestamps
        if 'start_time' in data:
            start_time = data.pop('start_time')
            start_time_obj = datetime.fromtimestamp(start_time / 1000)
            print(f'time is ====> {start_time_obj}')
            data['start_time'] = start_time_obj

        return data

    class Meta:
        model = Initial
        fields = '__all__'
        depth = 1


class InvestRecordSerializer(serializers.ModelSerializer):
    """
    投资记录序列化
    """

    # 基金模型不可编辑
    # 前端传入基金id 后台通过id查询基金模型 进行数据的创建及更新
    fund = AssetTypeSerializer(read_only=True)
    date_time = serializers.DateTimeField(format="%s.%f")

    def validate_fund(self, value):
        """
        自定义 fund 字段的校验
        id 只判断类型 & 数据是否存在
        """
        if type(value) == 'int':
            raise serializers.ValidationError("Field fund type is not int.")

        try:
            fund = AssetType.objects.get(pk=value)
        except AssetType.DoesNotExist:
            raise serializers.ValidationError(f'Fund {value} dose not exist.')

        return value

    def to_internal_value(self, data):
        """
        修改反序列化行为
        由于fund参数为id 需要将其转换成对应的fund数据 所以使用此方法进行转换
        """
        if 'fund' in data:
            fund_id = data.pop('fund', None)
            try:
                fund = AssetType.objects.get(pk=fund_id)
            except AssetType.DoesNotExist:
                raise serializers.ValidationError(f'Fund {fund_id} dose not exist.')

            data['fund'] = fund

        # 转换start_time
        # 前端传入timestamps为毫秒级 需要转换成python的秒级timestamps
        if 'date_time' in data:
            date_time = data.pop('date_time')
            date_time_obj = datetime.fromtimestamp(date_time / 1000)
            data['date_time'] = date_time_obj

        return data

    class Meta:
        model = InvestRecord
        fields = '__all__'
        depth = 1


from rest_framework import serializers
from .models import Asset, AssetType, AssetCategory, Bucket, Sex, Investor
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from django.contrib.auth import authenticate, user_logged_in


class BucketSerializer(serializers.ModelSerializer):

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
        fields = ('name', 'code', 'category')


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
        fields = ('id', 'type', 'owner', 'amount')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class JWTSerializer(JSONWebTokenSerializer):
    """
    Create a custom serializer inherit JSONWebTokenSerializer
    """
    def validate(self, attrs):
        credential = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credential.values()):
            user = authenticate(request=self.context['request'], **credential)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
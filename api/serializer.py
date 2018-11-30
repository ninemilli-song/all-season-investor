from rest_framework import serializers
from .models import Asset, AssetType, AssetCategory, Bucket, Sex, Investor
from django.contrib.auth.models import User


class BucketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bucket
        fields = '__all__'


class AssetCategorySerializer(serializers.ModelSerializer):
    bucket = BucketSerializer()

    class Meta:
        model = AssetCategory
        fields = ('name', 'code', 'bucket')


class AssetTypeSerializer(serializers.ModelSerializer):
    type = AssetCategorySerializer()

    class Meta:
        model = AssetType
        fields = ('name', 'code', 'type')


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

    class Meta:
        model = Investor
        fields = '__all__'



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
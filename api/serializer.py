from rest_framework import serializers
from .models import Asset, User, AssetType, AssetCategory, Bucket


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    type = AssetTypeSerializer()

    class Meta:
        model = Asset
        fields = ('type', 'owner', 'amount')
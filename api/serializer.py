from rest_framework import serializers
from .models import Asset, User, AssetType, AssetCategory, Bucket, Sex


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
    sex = serializers.SlugRelatedField(
        read_only=True,
        slug_field='label'
    )

    class Meta:
        model = User
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    type = AssetTypeSerializer(read_only=True)

    class Meta:
        model = Asset
        fields = ('type', 'owner', 'amount')

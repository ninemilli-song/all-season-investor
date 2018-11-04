from django.urls import path

from . import views

# 命名空间
app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('asset-view/<int:user_id>/', views.assetView, name='assetView'),
    path('assetByUser/<pk>/', views.AssetByUser.as_view(), name='user-asset'),
    path('usersAssetList/', views.UsersAssetList.as_view(), name='users-asset-list')
]

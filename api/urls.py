from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'investors', views.Investors, basename='investors-list')
router.register(r'assets', views.InvestorAssets, basename='assets')

# 命名空间
app_name = 'api'
urlpatterns = [
    # path('', views.index, name='index'),
    path('asset-view/<int:user_id>/', views.assetView, name='assetView'),
    # path('userDetail/<pk>/', views.UserDetail.as_view(), name='user-asset-detail'),
    # path('userList/', views.UserList.as_view(), name='users-asset-list'),
    # path('updateAsset/<int:user>/<int:asset>', views.UpdateAssetAmount.as_view())
]

urlpatterns += router.urls



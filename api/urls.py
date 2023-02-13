from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = DefaultRouter()
router.register(r'investors', views.Profile, basename='investors-list')
router.register(r'assets', views.InvestorAssets, basename='assets')
router.register(r'profile', views.Profile, basename='profile')
router.register(r'initial', views.InitialView, basename='initial')
router.register(r'fund', views.FundView, basename='fund')
router.register(r'invest-record', views.InvestRecordView, basename='invest-record')

# 命名空间
app_name = 'api'
urlpatterns = [
    # path('', views.index, name='index'),
    path('asset-view/<int:user_id>/', views.asset_view, name='asset_view'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/login/', views.LoginView.as_view(), name='auth_login'),
    path('auth/userInfo/', views.UserInfo.as_view(), name='auth_user_info'),
    path('auth/signup/', views.signup, name='auth_signup'),
    path('fund-list/', views.FundListView.as_view(), name='fund_list')
]

urlpatterns += router.urls



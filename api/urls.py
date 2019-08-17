from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = DefaultRouter()
router.register(r'investors', views.Profile, basename='investors-list')
router.register(r'assets', views.InvestorAssets, basename='assets')
router.register(r'profile', views.Profile, basename='profile')
router.register(r'initial', views.InitialView, basename='initial')

# 命名空间
app_name = 'api'
urlpatterns = [
    # path('', views.index, name='index'),
    path('asset-view/<int:user_id>/', views.assetView, name='assetView'),
    path('token/', obtain_jwt_token, name='token_obtain_pair'),
    path('token/refresh', refresh_jwt_token, name='token_refresh'),
    path('token/verify', verify_jwt_token, name='token_verify'),
    path('auth/login/', views.LoginView.as_view(), name='auth_login'),
    path('auth/userInfo/', views.UserInfo.as_view(), name='auth_user_info'),
    path('auth/signup/', views.signup, name='auth_signup')
]

urlpatterns += router.urls



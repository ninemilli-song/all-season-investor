from django.urls import path

from . import views

# 命名空间
app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('asset/<int:user_id>/', views.asset, name='asset'),
    path('asset-view/<pk>/', views.AssetView.as_view(), name='assetView')
]

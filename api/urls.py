from django.urls import path

from . import views

# 命名空间
app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('asset-view/<int:user_id>/', views.assetView, name='assetView'),
    path('asset/<pk>/', views.assest.as_view(), name='asset')
]

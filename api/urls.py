from django.urls import path

from . import views

# 命名空间
app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('asset-view/<int:user_id>/', views.assetView, name='assetView'),
    path('userDetail/<pk>/', views.UserDetail.as_view(), name='user-asset-detail'),
    path('userList/', views.UserList.as_view(), name='users-asset-list')
]

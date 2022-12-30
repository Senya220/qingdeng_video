
from django.urls import path
from .base import Index
from .views import Login, AdminManager

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login/', Login.as_view(), name='dashboard_login'),
    path('admin/manager/', AdminManager.as_view(), name='admin_manager'),
]

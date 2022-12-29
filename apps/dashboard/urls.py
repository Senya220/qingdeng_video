
from django.urls import path
from .base import Index
from .views import Login

urlpatterns = [
    path('index/', Index.as_view(), name='dashboard_index'),
    path('login/', Login.as_view(), name='dashboard_login'),
    path('admin/manager/', Login.as_view(), name='admin_manager'),
]

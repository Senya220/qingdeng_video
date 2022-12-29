
from django.urls import path
from .base import Base

urlpatterns = [
    path('base/', Base.as_view()),
]
